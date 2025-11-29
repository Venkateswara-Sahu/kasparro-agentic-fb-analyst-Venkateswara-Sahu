# Agent Graph: Kasparro Agentic FB Ads Analyst

## Overview
A multi-agent system for autonomous Facebook Ads performance analysis, using LLM-driven reasoning to diagnose ROAS fluctuations, generate insights, and propose creative improvements.

## Agent Roles & Data Flow

1. **Planner Agent**
   - Input: User query (string)
   - Output: Plan (dict with query, steps)
   - Role: Decompose query into subtasks

2. **Data Agent**
   - Input: Raw data (DataFrame), Plan (dict)
   - Output: Processed summary (dict with metrics, trends)
   - Role: Load, clean, and summarize dataset

3. **Insight Agent**
   - Input: Processed data (dict), Plan (dict)
   - Output: Insights (list of hypotheses with confidence, evidence)
   - Role: Generate hypotheses explaining patterns

4. **Evaluator Agent**
   - Input: Insights (list)
   - Output: Evaluated insights (filtered list)
   - Role: Validate with quantitative checks

5. **Creative Generator**
   - Input: Evaluated insights (list), Plan (dict)
   - Output: Creatives (list of recommendations)
   - Role: Propose new ad creatives for low-CTR campaigns

## Data Flow Diagram

```
User Query
    ↓
Planner → Plan
    ↓
Data Agent ← Raw Data → Processed Data
    ↓
Insight Agent → Insights
    ↓
Evaluator → Evaluated Insights
    ↓
Creative Generator → Creatives
    ↓
Report Generation
```

## LLM Integration
- Uses local Gemma 3 4B via Ollama for cost-effective, private inference
- Fallback to OpenAI, Anthropic, Gemini if configured
- Structured prompts with Think-Analyze-Conclude for reasoning

## Observability
- JSON logs in logs/agent_run.log
- Reports in reports/ (insights.json, creatives.json, report.md)