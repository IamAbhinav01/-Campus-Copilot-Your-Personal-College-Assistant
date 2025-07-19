from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

if os.getenv("LANGSMITH_TRACING", "false").lower() == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")

class Assistant:
    def __init__(self):
        self.llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model="moonshotai/kimi-k2-instruct")
        
    def build_prompt(self, query, events):
        event_list = "\n".join([f"{e.title} from {e.start_time.strftime('%Y-%m-%d %H:%M')} to {e.end_time.strftime('%Y-%m-%d %H:%M')}" for e in events])
        prompt = f"""
You are a personal college assistant. Here are the user's upcoming events:

{event_list}

Answer the following query based on this schedule:
{query}
"""
        return prompt.strip()

    def run(self, query, events):
        prompt = self.build_prompt(query, events)
        response = self.llm([HumanMessage(content=prompt)])
        return response.content
