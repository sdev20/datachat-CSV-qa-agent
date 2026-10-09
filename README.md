# HelloAgent

A small Streamlit app that lets you ask questions across multiple CSV files in plain English. It uses a LangChain pandas DataFrame agent backed by OpenAI (`gpt-4o-mini`): the agent writes and runs pandas code against your uploaded data and replies with the answer.

## Project structure

```
HelloAgent-AgenticAI/
├── HelloAgent_streamlit.py   # Streamlit app
├── Datasets/                 # Sample CSVs to upload
│   ├── saas_docs.csv
│   ├── credit_card_terms.csv
│   ├── hospital_policy.csv
│   └── ecommerce_faqs.csv
├── requirements.txt
├── .vscode/launch.json       # F5 run/debug config for Streamlit
└── .env                      # Your API key (not committed)
```

## Setup

1. **Create a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   In VS Code, run **Python: Select Interpreter** and pick `.venv/bin/python`.

2. **Install dependencies**

   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Add your OpenAI API key**

   Create a `.env` file in the project root:

   ```
   OPENAI_APIKEY=sk-your-key-here
   ```

   `.env` is listed in `.gitignore`, so it won't be committed. Never put the key in the code.

## Run

From the project folder:

```bash
python -m streamlit run HelloAgent_streamlit.py
```

The app opens at http://localhost:8501. Stop it with `Ctrl+C`.

In VS Code you can instead open `HelloAgent_streamlit.py` and press **F5** (uses `.vscode/launch.json`).

> Streamlit apps can't be started with the plain ▶ Run button or `python HelloAgent_streamlit.py`.

## Usage

1. Upload one or more CSV files (try the ones in `Datasets/`).
2. Type a question in the **Ask a question** box and press Enter.
3. The answer appears below.

Example questions:

- What is the visiting hour in the hospital?
- What is the API limit?

## Notes

- The system prompt in `HelloAgent_streamlit.py` assumes the four sample datasets. Edit it if you upload different files.
- `create_pandas_dataframe_agent` executes LLM-generated Python on your machine (`allow_dangerous_code=True`). Use it locally with your own data only; don't expose it to untrusted users.

