import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
from src.mcq_generator.logger import logging

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

LLM = ChatGoogleGenerativeAI(
    temperature=0.7, 
    model="gemini-2.0-flash", 
    max_output_tokens=5124, 
    google_api_key=google_api_key
    )

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template)

# quiz_chain = LLMChain(llm=LLM, 
#                       prompt=quiz_generation_prompt, 
#                       output_key="quiz", 
#                       verbose=True)

# template2="""
# You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
# You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
# if the quiz is not at per with the cognitive and analytical abilities of the students,\
# update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
# Quiz_MCQs:
# {quiz}

# Check from an expert English Writer of the above quiz:
# """


# quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=template2)

# review_chain=LLMChain(llm=LLM, 
#                       prompt=quiz_evaluation_prompt, 
#                       output_key="review", 
#                       verbose=True)


# # This is an Overall Chain where we run the two chains in Sequence
# generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], 
#                                         input_variables=["text", "number", "subject", "tone", "response_json"],
#                                         output_variables=["quiz", "review"], verbose=True,)

quiz_evaluation_template = PromptTemplate(
    input_variables=["subject", "quiz"],
    template="""
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. \
If the quiz is not at par with the cognitive and analytical abilities of the students, \
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities.

Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
)

# LCEL Chains

# Step 1: Quiz generation
generate_quiz_chain = quiz_generation_prompt | LLM

# Step 2: Combine input and quiz output
combine_inputs = RunnableMap({
    "subject": lambda x: x["subject"],
    "quiz": generate_quiz_chain
})

# Step 3: Quiz evaluation
evaluate_quiz_chain = combine_inputs | quiz_evaluation_template | LLM

# Final pipeline: LCEL RunnableSequence
# generate_and_evaluate_chain = RunnableSequence([
#     RunnableMap(lambda x: x),   # Pass-through to preserve all inputs
#     RunnableMap({
#         "quiz": generate_quiz_chain,
#         "subject": lambda x: x["subject"]
#     }),
#     quiz_evaluation_template | LLM
# ])

# from langchain_core.runnables import RunnableMap

generate_and_evaluate_chain = (
    RunnableMap({
        "text": lambda x: x["text"],
        "number": lambda x: x["number"],
        "subject": lambda x: x["subject"],
        "tone": lambda x: x["tone"],
        "response_json": lambda x: x["response_json"]
    })
    | RunnableMap({
        "quiz": generate_quiz_chain,
        "subject": lambda x: x["subject"]
    })
    | (quiz_evaluation_template | LLM)
)


# # Example usage
# if __name__ == "__main__":
#     input_data = {
#         "text": "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll.",
#         "number": 3,
#         "subject": "Biology",
#         "tone": "engaging",
#         "response_json": '{"questions": [{"question": "", "options": ["", "", "", ""], "answer": ""}]}'
#     }

#     result = generate_and_evaluate_chain.invoke(input_data)
#     print("Review Output:\n", result.content)