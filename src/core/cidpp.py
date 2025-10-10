import json

def compute_cidpp_score(evaluation: dict) -> dict:
    scores = {k: v for k, v in evaluation.items() if isinstance(v, dict) and 'score' in v}
    average = sum(s['score'] for s in scores.values()) / len(scores) if scores else 0
    return {
        "scores": scores,
        "average": average
    }

def compute_cidpp_score_simple(evaluation: dict) -> float:
    return sum(evaluation.values()) / len(evaluation) if evaluation else 0
