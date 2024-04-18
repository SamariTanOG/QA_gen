import os
import json
import pandas as pd
import traceback
import getpass
import os
import streamlit as st

#inputting number of questions to be generated and the input is taken directly from user 
NUMBER = st.number_input('Enter Number of questions to be created')
st.write('The current number is ', NUMBER)


#inputting Difficulty level of questions and the input is taken directly from user 
TONE = st.text_input('Enter Difficulty of questions')
st.write('Difficulty is set to', TONE)

#loading google gemini pro model 
#NOTE if you are trying to run the code it wont unless you put an API key as i will be replacing the API KEY
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("'AIzaSyC8b2RW7aBL4w2L7EnION-7TBrarb85N60'")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

import PyPDF2

#Initiating and defining model
llm = ChatGoogleGenerativeAI(model="gemini-pro")


RESPONSE_JSON = {
    "1": {
        "question": "Answer",
        
    },
    "2": {
        "question": "Answer",
    },
    "3": {
        "question": "Answer",
    },
}
#setting template
TEMPLATE="""
Text:{text}
You are an expert in generating question and answers over provided text.
Given the above text, it is your job to create question  of {number}  in {tone} tone with their answers. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. 
Ensure to make {number} of questions with their answers in provided {tone}
### RESPONSE_JSON
{response_json}

"""

qaa_generation_prompt = PromptTemplate(
    input_variables=["text", "number",  "tone", "response_json"],
    template=TEMPLATE
    )
qa_chain=LLMChain(llm=llm, prompt=qaa_generation_prompt, output_key="qa_gen", verbose=True)
TEMPLATE2="""
You are an expert english grammarian and writer. Given a set of question with their answers.
if you find any grammatical mistakes do correct them and if you find any question or answer to be incorrect do correct it
QA_GEN:
{qa_gen}

Check from an expert English Writer of the above questions:
"""
qa_evaluation_prompt=PromptTemplate(input_variables=["subject", "qa_gen"], template=TEMPLATE)
review_chain=LLMChain(llm=llm, prompt=qa_evaluation_prompt, output_key="review", verbose=True)
generate_evaluate_chain=SequentialChain(chains=[qa_chain, review_chain], input_variables=["text", "number", "tone", "response_json"],
                                        output_variables=["qa_gen", "review"], verbose=True,)
file_path=r"./Big Mac Index.pdf"
with open(file_path, 'r', errors='ignore') as file:
    TEXT = file.read()
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(file_path)
data = loader.load_and_split()
json.dumps(RESPONSE_JSON)
#NUMBER=5 

#TONE="simple"

#since the loaded pdf contains a lot of other unnecessary texts we will append them with respect to page number
documents = ""
for c in data:
    text = c.page_content  # Access text from 'page_content'
    documents += text


response=generate_evaluate_chain(
        {
            "text": documents,
            "number": NUMBER,
            
            "tone": TONE,
            "response_json": json.dumps(RESPONSE_JSON)
        }
        )


qa=response.get("qa_gen")
import json

# Assuming quiz is the provided string
qa_data_start_index = qa.find('{')  # Find the starting index of the JSON data
json_data = qa[qa_data_start_index:]  # Extract the JSON data (excluding the header)

try:
    qa = json.loads(json_data)
    print(qa)
except json.JSONDecodeError as e:
    print(f"Error: {e}")

for key , value in qa.items():
    print(key,'\n',value)
file_path = "data.txt"

# Opening the file in write mode
with open(file_path, 'w') as file:
    # Iterating over the dictionary items and writing them to the file
    for key, value in qa.items():
        file.write(f"Question {key}: {value['question']}\n")
        file.write(f"Answer {key}: {value['answer']}\n\n")

print(qa)
print(json_data)

import streamlit as st
st.write(qa)
