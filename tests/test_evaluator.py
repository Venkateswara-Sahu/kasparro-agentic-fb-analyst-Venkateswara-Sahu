import pytest
from src.agents.evaluator import Evaluator

def test_evaluator_high_confidence():
    config = {'confidence_min': 0.6}
    evaluator = Evaluator(config)
    insights = [
        {'hypothesis': 'Test', 'confidence': 0.8},
        {'hypothesis': 'Low', 'confidence': 0.4}
    ]
    result = evaluator.evaluate(insights)
    assert len(result) == 1
    assert result[0]['confidence'] == 0.8

def test_evaluator_no_insights():
    config = {'confidence_min': 0.6}
    evaluator = Evaluator(config)
    insights = []
    result = evaluator.evaluate(insights)
    assert result == []