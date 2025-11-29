"""
Data Agent: Loads, filters, and summarizes Facebook Ads dataset.
"""

import pandas as pd
from datetime import datetime, timedelta

class DataAgent:
    """
    Agent for data processing and summarization.
    
    Attributes:
        config (dict): Configuration settings
    """
    def __init__(self, config):
        self.config = config
    
    def process(self, data, plan):
        """
        Process and summarize the dataset based on the plan.
        
        Args:
            data (pd.DataFrame): Raw data
            plan (dict): Plan from planner
            
        Returns:
            dict: Processed data summary
        """
        # Ensure date is datetime
        data['date'] = pd.to_datetime(data['date'])
        
        # Calculate metrics if needed
        if 'roas' not in data.columns:
            data['roas'] = data['revenue'] / data['spend']
        if 'ctr' not in data.columns:
            data['ctr'] = (data['clicks'] / data['impressions']) * 100
        
        # Recent data (last 7 days)
        recent = data[data['date'] >= (data['date'].max() - timedelta(days=7))]
        
        # Summary
        summary = {
            "total_impressions": int(data['impressions'].sum()),
            "total_clicks": int(data['clicks'].sum()),
            "total_spend": float(data['spend'].sum()),
            "total_revenue": float(data['revenue'].sum()),
            "avg_roas": float(data['roas'].mean()),
            "avg_ctr": float(data['ctr'].mean()),
            "recent_avg_roas": float(recent['roas'].mean()) if not recent.empty else 0.0,
            "recent_avg_ctr": float(recent['ctr'].mean()) if not recent.empty else 0.0,
            "roas_trend": [float(x) for x in data.groupby('date')['roas'].mean().tolist()],
            "low_ctr_campaigns": data[data['ctr'] < 1]['campaign_name'].unique().tolist(),
            "top_platforms": data.groupby('platform')['revenue'].sum().to_dict(),
            "creative_performance": data.groupby('creative_type')['roas'].mean().to_dict()
        }
        
        return summary