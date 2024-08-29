import json
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.prompts import PromptTemplate

from langchain_openai import ChatOpenAI
from app.sandbox import execute_function
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt_template = PromptTemplate(
    input_variables=["user_question"],
    template="""
    You are an intelligent assistant. Based on the user question, determine which function to call and the parameters needed.
    
    User question: {user_question}
    
    Available functions:
    - calculate_sum(numbers: list of int): Calculate the sum of the numbers.
    - reverse_string(text: str): Reverse the given string.
    - generate_greeting(name: str): Generate a greeting message for the given name.
    - multiply_numbers(a: int, b: int): Multiply two numbers and return the result.
    - get_time(): Return the current time.

    Based on the user question, return the function name and parameters in JSON format.
    """
)


def create_langchain_model():
    llm = ChatOpenAI(temperature=0.9, name='gpt-3.5-turbo')
    chain = prompt_template | llm
    return chain

def process_user_request(user_question):
    langchain_model = create_langchain_model()
    response = langchain_model.invoke(user_question)
    content = response.content
    
    function_call_data = json.loads(content)

    function_name = function_call_data.get("function")
    function_args = function_call_data.get("parameters", {})

    return execute_function(function_name, function_args)