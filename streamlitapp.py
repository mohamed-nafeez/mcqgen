import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator import logger
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain

with open(r"C:\Users\hp\mcqgen\response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.write("The AI Question Generator App")

with st.form("user_form"):
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

    mcq_count = st.number_input("Number of MCQs to generate", min_value=1, max_value=10, value=5)

    subject = st.text_input("Subject", value="Mathematics")

    tone = st.text_input("Tone", placeholder="simple,difficult,medium", value="simple")

    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            response = None
            try:
                # Read file contents
                text = read_file(uploaded_file)

                # Call Gemini chain directly
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while processing the file.")

            else:
                # ✅ This block runs only if there was NO error
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        if isinstance(quiz, dict):
                            quiz_json = quiz
                        elif isinstance(quiz, str) and quiz.strip():
                            try:
                                quiz_json = json.loads(quiz)
                            except json.JSONDecodeError:
                                st.error("Quiz data is not valid JSON. Please check the model output.")

                    if quiz_json:
                        table_data = get_table_data(json.dumps(quiz_json))

                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            st.text_area(
                                label="Review",
                                value=response.get("review", "")
                            )
                        else:
                            st.error("Error in the table data.")

                    else:
                        st.write("No quiz found or quiz data could not be parsed.")
                else:
                    st.write(response)
