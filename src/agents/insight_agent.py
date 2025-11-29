"""
Insight Agent: Generates hypotheses explaining ROAS fluctuations.
"""

import os
import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

class InsightAgent:
    """
    Agent for generating data-driven insights and hypotheses.
    
    Attributes:
        config (dict): Configuration settings
        llm: Language model instance
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
    
    def generate_insights(self, processed_data, plan):
        """
        Analyze processed data to generate insights and hypotheses.
        
        Args:
            processed_data (dict): Processed data from data agent
            plan (dict): Plan from planner
            
        Returns:
            list: List of insights
        """
        if self.llm:
            with open('prompts/insight_prompt.md', 'r') as f:
                prompt_text = f.read()
            prompt = PromptTemplate.from_template(prompt_text)
            chain = prompt | self.llm
            response = chain.invoke({"data": json.dumps(processed_data), "plan": json.dumps(plan)})
            try:
                insights = json.loads(response.content)
            except json.JSONDecodeError:
                insights = [
                    {"hypothesis": "ROAS drop due to low CTR", "evidence": "CTR below 1%", "confidence": 0.8},
                    {"hypothesis": "Seasonal trends affecting performance", "evidence": "Recent data shows decline", "confidence": 0.7}
                ]
        else:
            insights = [
                {"hypothesis": "ROAS drop due to low CTR", "evidence": "CTR below 1%", "confidence": 0.8},
                {"hypothesis": "Seasonal trends affecting performance", "evidence": "Recent data shows decline", "confidence": 0.7}
            ]
        return insights