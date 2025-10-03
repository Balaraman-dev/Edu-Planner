def compute_ciddp_score(evaluation: dict) -> float:
    # return sum(evaluation.values()) / len(evaluation)  # avg of C,I,D,P,P
    return sum(evaluation.values()) / 1