from typing import List

def score(row):
    """Scoring function based on 3 metrics. The larger score is better."""
    latency_in_ms = get_latency(row)
    top1_match_rate = float(row["top1_match_rate"])
    onnx_size_in_MB = float(row["onnx_size_in_MB"])  # noqa: N806
    # A simple scoring function: cost of 0.1ms latency ~ 0.1% match rate ~ 100MB size
    return top1_match_rate * 1000 - latency_in_ms * 10 - onnx_size_in_MB / 100


def score(
    quality_sample: float,
    model_cost: float,
    all_costs: List[float],
    quality_weight: float = DEFAULT_QUALITY_WEIGHT,
    cost_weight: float = DEFAULT_COST_WEIGHT,
) -> float:
    """
    Multi-objective score. V0 is a weighted linear sum of (quality, normalized_cost).
    Higher is better. Both inputs are in [0, 1].
    """
    cost_score = normalized_cost(model_cost, all_costs)
    return quality_weight * quality_sample + cost_weight * cost_score


def score(hand):
    """Returns the score for a hand(0 if a bust)."""
    return (jnp.logical_not(is_bust(hand))) * sum_hand(hand)


def score(hand):  # What is the score of this hand (0 if bust)
    return 0 if is_bust(hand) else sum_hand(hand)


def score(hand):  # What is the score of this hand (0 if bust)
    return 0 if is_bust(hand) else sum_hand(hand)

