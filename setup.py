from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Jesuyanmife Egbewale',
    author_email='Egbewaleyanmife@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","google-genai","langchain-google-genai"],
    packages=find_packages()
)