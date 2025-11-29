# Kasparro Agentic FB Analyst

An agentic AI system for analyzing Facebook Ads performance using multi-agent reasoning with local LLMs.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Ensure Ollama is running with Gemma 3 4B: `ollama run gemma3:4b`
3. Run: `python src/run.py "Analyze the Facebook Ads data"`

## Architecture

- Planner: Plans the analysis
- Data Agent: Processes data
- Insight Agent: Generates hypotheses
- Evaluator: Validates insights
- Creative Generator: Suggests improvements

Outputs in `reports/` and logs in `logs/`.