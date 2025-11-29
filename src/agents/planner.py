"""
Planner Agent: Decomposes user queries into structured subtasks for the agentic system.
"""

import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import os

class Planner:
    """
    Agent responsible for planning the analysis workflow.
    
    Attributes:
        config (dict): Configuration settings
        llm: Language model instance (if API key available)
    """
    def __init__(self, config):
        self.config = config
        if config.get('use_local_model'):
            self.llm = ChatOllama(model=config.get('local_model_name', 'gemma3:4b'), temperature=0.1)
        elif config.get('anthropic_api_key'):
            os.environ['ANTHROPIC_API_KEY'] = config['anthropic_api_key']
            self.llm = ChatAnthropic(temperature=0.1, model="claude-3-sonnet-20240229")
        elif config.get('openai_api_key'):
            os.environ['OPENAI_API_KEY'] = config['openai_api_key']
            self.llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
        elif config.get('gemini_api_key'):
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config['gemini_api_key'], temperature=0.1)
        else:
            self.llm = None
    
    def plan(self, query):
        """
        Generate a structured plan for the given query.
        
        Args:
            query (str): User query
            
        Returns:
            dict: Plan with query and steps
        """
        if self.llm:
            with open('prompts/planner_prompt.md', 'r') as f:
                prompt_text = f.read()
            prompt = PromptTemplate.from_template(prompt_text)
            chain = prompt | self.llm
            response = chain.invoke({"query": query})
            try:
                plan = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback if not JSON
                plan = {
                    "query": query,
                    "steps": [
                        "Load and preprocess data",
                        "Analyze ROAS over time",
                        "Identify drops in last 7 days",
                        "Generate insights on causes",
                        "Evaluate insights",
                        "Generate creative suggestions"
                    ]
                }
        else:
            plan = {
                "query": query,
                "steps": [
                    "Load and preprocess data",
                    "Analyze ROAS over time",
                    "Identify drops in last 7 days",
                    "Generate insights on causes",
                    "Evaluate insights",
                    "Generate creative suggestions"
                ]
            }
        return plan