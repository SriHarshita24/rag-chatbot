import pandas as pd
import requests
from tabulate import tabulate
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_1 = "llama3"
MODEL_2 = "deepseek-r1"

df = pd.read_csv("cleaned_exoplanet_dataset.csv")

df = df[[
    "pl_name",
    "hostname",
    "pl_bmassj",
    "pl_radj",
    "discoverymethod",
    "disc_year"
]]

df = df.dropna(subset=["pl_bmassj", "disc_year"])

VALID_COLUMNS = [c.lower() for c in df.columns]

def dataset_intro():
    print("\n EXOPLANET DATASET OVERVIEW")
    print("--------------------------------------------------")
    print(f"Total planets: {len(df)}")
    print(f"Year range: {df['disc_year'].min()} - {df['disc_year'].max()}")
    print(f"Average mass: {round(df['pl_bmassj'].mean(),2)} Jupiter masses")
    print("Main discovery methods:", df["discoverymethod"].value_counts().head(3).to_dict())
    print("--------------------------------------------------\n")

def check_invalid_attribute(user_query):
    q = user_query.lower()

    stopwords = {
        "with", "and", "or", "after", "before", "using",
        "planets", "planet", "largest", "smallest",
        "show", "list", "get", "give", "me",
        "what", "which", "who", "is", "are",
        "the", "a", "an", "of", "in", "on",
        "mass", "year", "method", "transit", "radial"
    }

    words = re.findall(r"[a-zA-Z_]+", q)

    for word in words:
        if word in stopwords:
            continue

        if not any(word in col for col in VALID_COLUMNS):
            return word

    return None

def ask_llm(model, prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            print(f"API Error ({model}):", response.status_code)
            return ""

        text = response.json().get("response", "")

        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL
        )

        return text.strip()

    except Exception as e:
        print(f"LLM Error ({model}):", e)
        return ""

def clean_query(text):
    if not text:
        return ""

    text = re.sub(r"```python|```", "", text)

    for line in text.split("\n"):
        if "df" in line:
            return line.strip()

    return ""

def generate_query(user_query):
    prompt = f"""
Convert question to pandas query.

Use only df. One line.

Columns: {df.columns.tolist()}

Question: {user_query}
"""
    return ask_llm(MODEL_1, prompt), ask_llm(MODEL_2, prompt)

def smart_query(user_query):
    q = user_query.lower()
    result = df.copy()

    if "after" in q:
        try:
            year = int(re.findall(r'\d+', q)[0])
            result = result[result["disc_year"] > year]
        except:
            pass

    if "transit" in q:
        result = result[result["discoverymethod"].str.contains("Transit", na=False)]

    if "radial" in q:
        result = result[result["discoverymethod"].str.contains("Radial", na=False)]

    if "largest" in q or "mass" in q:
        result = result.sort_values(by="pl_bmassj", ascending=False)

    return result if not result.empty else None

def run_query(query):
    try:
        result = eval(query, {"__builtins__": {}}, {"df": df, "pd": pd})

        if isinstance(result, pd.Series):
            return result.to_frame().T

        return result
    except:
        return None

def summarize_results(data):

    table_text = data.head(10).to_string(index=False)

    prompt = f"""
You are a data analyst.

Analyze the following exoplanet query results.

Requirements:
- Write 2-3 concise sentences.
- Mention interesting trends.
- Mention masses if relevant.
- Mention discovery methods if relevant.
- Do not repeat the table.

Dataset Results:

{table_text}
"""

    print("\nGenerating Llama3 summary...")
    summary_llama = ask_llm(MODEL_1, prompt)

    print("\nGenerating DeepSeek summary...")
    summary_deepseek = ask_llm(MODEL_2, prompt)

    if not summary_llama:
        summary_llama = "Summary generation failed."

    if not summary_deepseek:
        summary_deepseek = "Summary generation failed."

    return summary_llama, summary_deepseek

def resolve_conflict(s1, s2):

    if not s1:
        return s2

    if not s2:
        return s1

    if s1.strip() == s2.strip():
        return "Both models agree:\n" + s1

    prompt = f"""
Two AI models analyzed the same dataset.

Summary 1:
{s1}

Summary 2:
{s2}

Compare the summaries.
If they contain different observations, combine them into a single
accurate summary.

Return only the final unified summary.
"""

    final_summary = ask_llm(MODEL_1, prompt)

    if final_summary.strip():
        return (
            "Discrepancy detected between models.\n"
            "Unified Summary:\n"
            + final_summary.strip()
        )

    return (
        "Discrepancy detected between models.\n\n"
        f"Model 1:\n{s1}\n\n"
        f"Model 2:\n{s2}"
    )
def chatbot():
    dataset_intro()

    print("Ask questions like:")
    print("- largest planets")
    print("- planets after 2015")
    print("- largest planets after 2015 using transit\n")

    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        invalid = check_invalid_attribute(question)
        if invalid:
            print(f" '{invalid}' is not a valid attribute in this dataset.")
            continue

        q1, q2 = generate_query(question)

        print("\n Llama3 Query:\n", q1)
        print("\n DeepSeek Query:\n", q2)

        result = smart_query(question)

        if result is not None:
            print(" Using smart query\n")
        else:
            query = clean_query(q1) or clean_query(q2)
            print("\n Selected Query:\n", query)
            result = run_query(query)

        if result is None or result.empty:
            print(" No results found")
            continue

        if len(result) > 10:
            print(" Too many results. Showing top 10. Consider refining your query.\n")
            result = result.head(10)

        print("\n Data:\n")
        print(tabulate(result, headers="keys", tablefmt="grid"))

        s1, s2 = summarize_results(result)

        print("\n Llama3:\n", s1)
        print("\n DeepSeek:\n", s2)

        print("\n Comparison")

        if q1 != q2:
            print("Query diff detected")

        if s1 != s2:
            print("Summary diff detected")

        final = resolve_conflict(s1, s2)

        print("\n Final:\n", final)

if __name__ == "__main__":
    chatbot()