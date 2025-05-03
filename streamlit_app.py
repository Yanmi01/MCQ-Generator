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

if button and uploaded_file and mcq_count and subject and tone:
    with st.spinner("Generating MCQs..."):
        try:
            text = read_file(uploaded_file)
            if text:
                result = generate_and_evaluate_chain.invoke({
                    "text": text, 
                    "number": mcq_count, 
                    "subject": subject, 
                    "tone": tone, 
                    "response_json": json.dumps(RESPONSE_JSON)
                })
                
                raw = result.content if hasattr(result, "content") else str(result)
                
                # Extract just the JSON portion from the output
                try:
                    # Find the start of the JSON (look for "{")
                    json_start = raw.find('{')
                    # Find the end of the JSON (look for the last "}")
                    json_end = raw.rfind('}') + 1
                    json_str = raw[json_start:json_end]
                    quiz = json.loads(json_str)
                except (ValueError, json.JSONDecodeError) as e:
                    st.error(f"Could not extract JSON from response: {e}")
                    st.text("Raw output for debugging:")
                    st.text(raw)
                    quiz = None
                
                if quiz:
                    # Transform the nested JSON into a flat structure
                    questions = []
                    for q_num, q_data in quiz.items():
                        if isinstance(q_data, dict):
                            question = {
                                "Question": q_data.get("mcq", ""),
                                "Option A": q_data.get("options", {}).get("a", ""),
                                "Option B": q_data.get("options", {}).get("b", ""),
                                "Option C": q_data.get("options", {}).get("c", ""),
                                "Option D": q_data.get("options", {}).get("d", ""),
                                "Correct Answer": q_data.get("correct", "")
                            }
                            questions.append(question)
                    
                    if questions:
                        df = pd.DataFrame(questions)
                        df.index = df.index + 1
                        
                        # Display the quiz
                        st.table(df)
                        
                        # Create download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Quiz as CSV",
                            data=csv,
                            file_name=f"{subject}_quiz.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error("No questions found in the quiz data")
                
        except Exception as e:
            st.error(f"Error generating the quiz: {e}")
            st.text(traceback.format_exc())