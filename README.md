# RAG Chatbot — Exoplanet Data Analysis

A Python-based AI chatbot that answers natural-language questions about exoplanets using a structured dataset and locally running Large Language Models (LLMs).

The project combines Pandas-based data analysis with Ollama-powered LLMs, Llama 3 and DeepSeek-R1, to generate data queries, summarize results, compare model outputs, and produce a unified response.

## Overview

This project allows users to explore an exoplanet dataset by asking questions in natural language. It processes the dataset using Pandas, applies filtering and sorting operations, and uses two LLMs to generate queries and analyze the resulting data.

The chatbot compares the responses from both models and attempts to resolve differences into a single summary.

## Features

- Natural-language queries for exoplanet data
- Dataset overview, including planet count, discovery-year range, average mass, and common discovery methods
- Data filtering and sorting using Pandas
- LLM-generated Pandas queries using Llama 3 and DeepSeek-R1
- Rule-based query handling for selected conditions
- Tabular output using the Tabulate library
- AI-generated summaries of query results
- Comparison of outputs from two language models
- Unified summaries when model responses differ
- Local LLM inference through Ollama

## Tech Stack

- **Python** — core application logic
- **Pandas** — dataset processing, filtering, and sorting
- **Ollama** — local LLM inference
- **Llama 3** — query generation and result summarization
- **DeepSeek-R1** — alternative query generation and summarization
- **Requests** — communication with the Ollama API
- **Tabulate** — formatted tabular output
- **Regular Expressions** — query validation and response cleaning
- **CSV** — structured exoplanet dataset

## How It Works

1. **Load the dataset:** Read `cleaned_exoplanet_dataset.csv` using Pandas.
2. **Prepare the data:** Select relevant columns and remove records missing planet mass or discovery year.
3. **Introduce the dataset:** Display summary statistics, discovery-year range, and common discovery methods.
4. **Validate user input:** Check whether query terms appear to reference valid dataset attributes.
5. **Generate queries:** Ask Llama 3 and DeepSeek-R1 to convert the natural-language question into a Pandas query.
6. **Retrieve results:** Apply supported rule-based filters or execute a selected generated query.
7. **Display data:** Present the results in a formatted table.
8. **Summarize results:** Ask both models to analyze the retrieved data.
9. **Compare responses:** Identify differences between generated queries and summaries.
10. **Resolve discrepancies:** Use Llama 3 to combine differing summaries into a unified response.

## Dataset

The project uses `cleaned_exoplanet_dataset.csv` and selects the following columns:

| Column | Description |
|---|---|
| `pl_name` | Planet name |
| `hostname` | Name of the host star |
| `pl_bmassj` | Planet mass in Jupiter-mass units |
| `pl_radj` | Planet radius in Jupiter-radius units |
| `discoverymethod` | Method used to discover the planet |
| `disc_year` | Year of discovery |

Records without a planet mass or discovery year are excluded during preprocessing.

## Getting Started

### Prerequisites

- Python 3.11 or a compatible Python version
- Git
- Ollama installed and running
- The required Ollama models downloaded locally

### Clone the Repository

```bash
git clone https://github.com/SriHarshita24/rag-chatbot.git
cd rag-chatbot
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
python -m pip install pandas requests tabulate
```

### Set Up Ollama

Install Ollama from the official website:

https://ollama.com/

Download the models used by the project:

```bash
ollama pull llama3
ollama pull deepseek-r1
```

Ensure Ollama is running and the local API at `http://localhost:11434` is accessible.

### Run the Chatbot

```bash
python project.py
```

Keep the dataset CSV file in the project directory so the script can load it.

## Example Questions

Try asking:

- `largest planets`
- `planets after 2015`
- `largest planets after 2015 using transit`

Type `exit` to stop the chatbot.

## Example Workflow

```text
User Question
      |
      v
Input Validation
      |
      v
Llama 3 + DeepSeek-R1
      |
      v
Query Generation / Rule-Based Filtering
      |
      v
Pandas Data Processing
      |
      v
Formatted Results Table
      |
      v
Two LLM-Generated Summaries
      |
      v
Response Comparison
      |
      v
Unified Final Summary
```

## Limitations

- Query generation and interpretation may fail for unsupported or ambiguous questions.
- Rule-based filtering handles only selected query patterns.
- The generated Pandas query may not correctly represent every natural-language request.
- Results depend on the completeness and quality of the dataset.
- Differences between model responses do not necessarily mean either model is correct.
- The application requires the Ollama service and both configured models to be available.

## Future Improvements

- Replace `eval()`-based query execution with a safer query-generation approach.
- Improve natural-language query parsing and filtering.
- Add automated tests for query generation and result accuracy.
- Add a graphical interface for easier interaction.
- Include dataset citations and clearer explanations of the results.
- Evaluate model responses against expected results.
- Add configuration options for model selection and generation parameters.

## Disclaimer

This project is intended for educational and experimental purposes. AI-generated summaries should be checked against the underlying dataset before being used for research or other decisions.
