"""
Creative Generator Agent: Produces new ad creatives for low-CTR campaigns.
"""

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import os
import json

class CreativeGenerator:
    """
    Agent for generating creative ad suggestions.
    
    Attributes:
        config (dict): Configuration settings
        llm: Language model instance
    """
    def __init__(self, config):
        self.config = config
        if config.get('use_local_model'):
            self.llm = ChatOllama(model=config.get('local_model_name', 'gemma3:4b'), temperature=0.7)
        elif config.get('anthropic_api_key'):
            os.environ['ANTHROPIC_API_KEY'] = config['anthropic_api_key']
            self.llm = ChatAnthropic(temperature=0.7, model="claude-3-sonnet-20240229")
        elif config.get('openai_api_key'):
            os.environ['OPENAI_API_KEY'] = config['openai_api_key']
            self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        elif config.get('gemini_api_key'):
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config['gemini_api_key'], temperature=0.7)
        else:
            self.llm = None
    
    def generate_creatives(self, evaluated_insights, plan):
        """
        Generate creative suggestions based on insights.
        
        Args:
            evaluated_insights (list): Evaluated insights
            plan (dict): Plan from planner
            
        Returns:
            list: Creative suggestions
        """
        if self.llm:
            with open('prompts/creative_prompt.md', 'r') as f:
                prompt_text = f.read()
            prompt = PromptTemplate.from_template(prompt_text)
            chain = prompt | self.llm
            response = chain.invoke({"insights": json.dumps(evaluated_insights), "plan": json.dumps(plan)})
            try:
                creatives = json.loads(response.content)
            except json.JSONDecodeError:
                creatives = [
                    {"campaign": "Ad1", "suggestion": "Improve ad copy for better CTR", "expected_impact": "Increase CTR by 20%"}
                ]
        else:
            creatives = [
                {"campaign": "Ad1", "suggestion": "Improve ad copy for better CTR", "expected_impact": "Increase CTR by 20%"}
            ]
        return creatives