import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_thread():
    client = openai.OpenAI()
    response = client.beta.threads.create()
    return response

def retrieve_thread(thread_id):
    client = openai.OpenAI()
    response = client.beta.threads.retrieve(thread_id)
    return response

def create_message(thread_id, role, content):
    client = openai.OpenAI()
    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )
    return response

def list_messages(thread_id):
    client = openai.OpenAI()
    response = client.beta.threads.messages.list(thread_id)
    return response

def create_run(thread_id, assistant_id, model="gpt-4", stream=True):
    client = openai.OpenAI()
    response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model=model,
        stream=stream
    )
    return response
