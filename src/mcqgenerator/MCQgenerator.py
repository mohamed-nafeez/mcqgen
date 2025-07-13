# %%
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Silence LangChain debug logs
#logging.getLogger("langchain").setLevel(logging.ERROR)

# %%
# Load your Gemini API Key
load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")

# %%
# Initialize Gemini LLM for LangChain
llm = ChatGoogleGenerativeAI(
    google_api_key=KEY,
    model="gemini-1.5-flash",
    temperature=0.5
)

# %%
# Prompt Template for quiz generation
TEMPLATE = """
Text:
{text}

You are an expert MCQ maker.

Given the above text, create a quiz of {number} multiple choice questions for {subject} students in a {tone} tone.

Rules:
- The questions must be strictly based on the provided text.
- The questions should not repeat.
- Your ENTIRE response MUST be a valid JSON object.
- Do NOT include any explanations, preamble, markdown, or additional text.
- Your JSON MUST start with open curly braces and end with close curly braces.
- Follow exactly the RESPONSE_JSON format below.

### RESPONSE_JSON
{response_json}

Ensure to make exactly {number} MCQs.
"""



# %%
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# %%
quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True
)

# %%
# Prompt Template for quiz review
TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity.

If the quiz is not at par with the cognitive and analytical abilities of the students,
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities.

Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""


# %%
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

# %%
review_chain = LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
    verbose=False
)

# %%
# Sequential Chain
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=False
)








