# MCQ Generator Using Langchain

A Streamlit-based application that generates Multiple Choice Questions (MCQs) from uploaded txt files or PDF documents using LLM-powered chains. Deployed live on AWS EC2!

## Live Demo
🌐 [Deployed on AWS EC2](http://3.137.164.110:8501)  

## Features

- Upload a `.pdf` or `.txt` file.
- Specify:
  - Number of MCQs
  - Subject
  - Complexity tone (e.g., simple, medium, difficult)
- MCQs are generated using a Langchain pipeline with evaluation.
- Review summary of the generated questions.
- Export MCQs as a downloadable CSV.

## Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python, Langchain
- **LLM Integration**: Gemini via Langchain
- **Deployment**: AWS EC2 (Ubuntu)
- **Virtual Environment**: `venv`
- **PDF Parsing**: PyPDF2
- **Environment Management**: `dotenv`

## local setup

```bash
# Clone the repo
git clone https://github.com/Yanmi01/MCQ-Generator.git
cd MCQ-Generator

# Create a virtual environment
python -m venv mcqgen
source mcqgen/bin/activate    # On Windows: mcqgen\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## Deployment on AWS EC2

Launch EC2 with a public IP and Ubuntu image.

```bash
# Connect to your AWS EC2 instance
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Navigate to your project directory
cd MCQ-Generator

# Activate the virtual environment
source mcqgen/bin/activate

# Run the Streamlit app
streamlit run streamlit_app.py
```

 ### Output
- MCQs displayed in a table format.

- Review summary provided.

- Option to download the quiz as a CSV file.

