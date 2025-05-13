from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm() -> ChatGoogleGenerativeAI:
    '''
    load a gemini llm
    '''
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
    if not os.environ["GOOGLE_API_KEY"]:
        raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return llm