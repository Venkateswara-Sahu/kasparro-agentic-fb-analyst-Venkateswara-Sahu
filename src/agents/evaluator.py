"""
Evaluator Agent: Validates insights with quantitative checks and confidence scoring.
"""

class Evaluator:
    """
    Agent for evaluating and scoring insights.
    
    Attributes:
        config (dict): Configuration settings
        min_confidence (float): Minimum confidence threshold
    """
    def __init__(self, config):
        self.config = config
        self.min_confidence = config['confidence_min']
    
    def evaluate(self, insights):
        """
        Evaluate insights for quality and assign confidence.
        
        Args:
            insights (list): List of insights
            
        Returns:
            list: Evaluated insights
        """
        evaluated = []
        for insight in insights:
            # Simple evaluation: if confidence > min, keep
            if insight.get('confidence', 0) >= self.min_confidence:
                evaluated.append(insight)
        return evaluated