#!/usr/bin/env python3

import sys
import os
import yaml
import pandas as pd
import json
import logging
from datetime import datetime
from agents.planner import Planner
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.evaluator import Evaluator
from agents.creative_generator import CreativeGenerator

# Setup logging
logging.basicConfig(filename='logs/agent_run.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_event(event, data):
    logger.info(f"{event}: {json.dumps(data, default=str)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/run.py 'query'")
        sys.exit(1)
    
    query = sys.argv[1]
    start_time = datetime.now()
    log_event("run_start", {"query": query, "timestamp": start_time.isoformat()})
    
    # Load config
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Load data
    data_path = config['data_csv']
    data = pd.read_csv(data_path)
    log_event("data_loaded", {"path": data_path, "rows": len(data)})
    
    # Initialize agents
    planner = Planner(config)
    data_agent = DataAgent(config)
    insight_agent = InsightAgent(config)
    evaluator = Evaluator(config)
    creative_generator = CreativeGenerator(config)
    
    # Plan
    plan = planner.plan(query)
    log_event("plan_generated", plan)
    
    # Process data
    processed_data = data_agent.process(data, plan)
    log_event("data_processed", processed_data)
    
    # Generate insights
    insights = insight_agent.generate_insights(processed_data, plan)
    log_event("insights_generated", insights)
    
    # Evaluate
    evaluated_insights = evaluator.evaluate(insights)
    log_event("insights_evaluated", evaluated_insights)
    
    # Generate creatives
    creatives = creative_generator.generate_creatives(evaluated_insights, plan)
    log_event("creatives_generated", creatives)
    
    # Save reports
    os.makedirs('reports', exist_ok=True)
    with open('reports/insights.json', 'w') as f:
        json.dump(evaluated_insights, f, indent=2)
    with open('reports/creatives.json', 'w') as f:
        json.dump(creatives, f, indent=2)
    
    # Generate report
    report = f"""
# Facebook Ads Analysis Report

**Query:** {query}

**Plan:** {plan['steps']}

**Key Metrics:**
- Total Impressions: {processed_data['total_impressions']}
- Total Clicks: {processed_data['total_clicks']}
- Avg ROAS: {processed_data['avg_roas']:.2f}
- Avg CTR: {processed_data['avg_ctr']:.2f}%

**Insights:**
{json.dumps(evaluated_insights, indent=2)}

**Creative Suggestions:**
{json.dumps(creatives, indent=2)}
"""
    with open('reports/report.md', 'w') as f:
        f.write(report)
    
    print("Analysis complete. Check reports/ and logs/")

if __name__ == "__main__":
    main()