import pandas as pd
import streamlit as st
import os
import sys
#import gdown
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv

load_dotenv()
print("Getting OPENAI API KEY..")
api_key = os.environ.get("OPENAI_APIKEY")

if not api_key:
    st.error("OPENAI_APIKEY is not set")
    st.stop()

# LOAD ALL CSVs INTO A LIST
dataframes = [] # We will store all the loaded tables here
loaded_names = []

st.header("Upload Multiple CSV Files")
uploaded_files = st.file_uploader(
    "Choose multiple CSV files", 
    type=["csv"], 
    accept_multiple_files=True
)

try:
    for file in uploaded_files:
        df = pd.read_csv(file)
        dataframes.append(df)
        loaded_names.append(file.name)
        print(f"SUCCESS: Loaded '{file.name}' ({len(df)} rows)")

except Exception as e:
    print(f"\nERROR loading files: {e}")
    sys.exit()

# 3. DEFINE THE RULES
system_prompt = """
You are a smart data assistant capable of reading multiple CSV files.
- You have access to 4 different datasets: SaaS Docs, Credit Card Terms, Hospital Policy, and Ecommerce FAQs.
- When asked a question, determine which DataFrame is most relevant.
- Do NOT answer from general knowledge.
- Answer in plain English.
"""

if not dataframes:
    st.info("Upload at least one CSV file to start asking questions.")
    st.stop()

st.success(f"Loaded {len(dataframes)} file(s): {', '.join(loaded_names)}")

try:
    # ---------------------------------------------------------
    # Initialize the LLM
    # ---------------------------------------------------------
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=api_key)

    # ---------------------------------------------------------
    # Create the Pandas Agent
    # Set verbose=True and allow_dangerous_code=True
    # ---------------------------------------------------------
    agent = create_pandas_dataframe_agent(
        llm,
        dataframes,
        verbose=True,
        agent_type="openai-functions",
        allow_dangerous_code=True,
        prefix=system_prompt
    )

except Exception as e:
    st.error(f"Error initializing agent: {e}")
    st.stop()

# ==========================================
#  ASK QUESTIONS
# ==========================================
st.header("Ask a question")
question = st.text_input(
    "Your question",
    placeholder="e.g. What is the visiting hour in the hospital?"
)

if question:
    with st.spinner("Thinking..."):
        try:
            result = agent.invoke({"input": question})
            st.write(result["output"])
        except Exception as e:
            st.error(f"Error: {e}")