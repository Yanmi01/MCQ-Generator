import os, json, traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging
from src.mcq_generator.MCQGenerator import generate_and_evaluate_chain
import streamlit as st


# with open("C:/Users/HP/personal_projects/AI_engineering/MCQ Generator/data/response.json", "r") as file:
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "data", "response.json")

with open(file_path, "r") as file:
    RESPONSE_JSON = json.load(file)

# st.title("MCQ Generator Application Using Langchain")
st.markdown("<h1 style='text-align: center;'>MCQ Generator Application Using Langchain</h1>", unsafe_allow_html=True)

# create a form using st.form
with st.form("user_input"):
    # file upload
    uploaded_file = st.file_uploader("Upload a pdf file or text", type=["pdf", "txt"])
    # input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=50)
    # subject
    subject = st.text_input("Subject", max_chars=30)
    # tone
    tone = st.text_input("Complexity of the Questions", max_chars=20, placeholder="simple") 
    
    # Add button
    button = st.form_submit_button("Create MCQs")   

    # check if the button is clicked and all fields have input
    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                # read the file
                text = read_file(uploaded_file)
                # check if the text is not empty
                if text:
                    # generate the quiz by invoking the chain
                    result = generate_and_evaluate_chain.invoke({
                        "text": text, 
                        "number": mcq_count, 
                        "subject": subject, 
                        "tone": tone, 
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
                    
                    # Handle the result (depending on whether it’s a string or dict)
                    raw = result.content if hasattr(result, "content") else str(result)
                    try:
                        quiz = json.loads(raw)  # attempt to parse as JSON
                    except json.JSONDecodeError:
                        quiz = raw  # if not JSON, treat as plain text

            except Exception as e:
                st.error(f"Error generating the quiz: {e}")
                st.text(traceback.format_exc())  # Show the full traceback
            else:
                # Process quiz result
                df = None  # Initialize df to None
                if isinstance(quiz, dict):
                    response = quiz.get("response", None)
                    if response:
                        questions = get_table_data(response)
                        if questions:
                            df = pd.DataFrame(questions)
                            df.index = df.index + 1  # to start the index at 1
                            # display the quiz table data in a table format
                            st.table(df)
    
                            st.text_area(label="Review", value = quiz['review'], height=200)

                        else:
                            st.error("Error converting the quiz to a table format")
                else:
                    st.write(quiz)  # Display raw quiz output (text or JSON)
                # Provide an option to download the quiz as a CSV file
                # if df is not None:
                #     csv = df.to_csv(index=False).encode('utf-8')
                #     st.download_button(
                #         label="Download Quiz as CSV",
                #         data=csv,
                #         file_name="quiz.csv",
                #         mime="text/csv",
                #     )
