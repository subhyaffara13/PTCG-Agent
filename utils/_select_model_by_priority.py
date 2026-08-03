from typing import Any, Dict, List, Optional

def _select_model_by_priority(
    model_names: List[str],
    model_preferences: "ModelPreferences",
) -> Optional[str]:
    """Score available models by MCP priority weights and return the best.

    Scoring strategy (per the MCP spec, priorities are 0-1 floats):

    * **costPriority** — higher means "prefer cheaper models".
      Metric: combined (input + output) cost per token from
      ``model_prices_and_context_window.json``.  Lower cost → higher score.

    * **speedPriority** — higher means "prefer faster models".
      Metric: ``output_tokens_per_second`` from model info when available;
      otherwise a neutral score for every candidate, since no reliable
      latency proxy exists (context-window size does not track speed).

    * **intelligencePriority** — higher means "prefer smarter models".
      Metric: ``max_output_tokens`` is used as a rough capability proxy
      (frontier models expose larger context windows).

    Each metric is min-max normalised across the candidate set so that
    every model gets a 0-1 score per dimension.  The final score is the
    weighted sum of the three normalised dimensions.

    Returns the highest-scoring model name, or None if scoring fails for
    all candidates (e.g. no model_info available).
    """
    import litellm as _litellm

    cost_weight = getattr(model_preferences, "costPriority", None) or 0.0
    speed_weight = getattr(model_preferences, "speedPriority", None) or 0.0
    intel_weight = getattr(model_preferences, "intelligencePriority", None) or 0.0

    # Gather raw metrics for each model
    scored: List[Dict[str, Any]] = []
    for name in model_names:
        try:
            info = _litellm.get_model_info(name)
        except Exception:
            continue
        input_cost = info.get("input_cost_per_token") or 0.0
        output_cost = info.get("output_cost_per_token") or 0.0
        total_cost = input_cost + output_cost
        max_output = info.get("max_output_tokens") or info.get("max_tokens") or 0
        output_tps = info.get("output_tokens_per_second") or 0.0
        scored.append(
            {
                "name": name,
                "cost": total_cost,
                "max_output": max_output,
                "output_tps": output_tps,
            }
        )

    if not scored:
        return None

    # Min-max normalisation helpers
    def _normalise(values: List[float], invert: bool = False) -> List[float]:
        """Normalise to [0, 1].  If *invert*, lower raw → higher score."""
        lo, hi = min(values), max(values)
        if hi == lo:
            return [0.5] * len(values)  # all equal → neutral score
        normed = [(v - lo) / (hi - lo) for v in values]
        if invert:
            normed = [1.0 - n for n in normed]
        return normed

    costs = [s["cost"] for s in scored]
    max_outputs = [float(s["max_output"]) for s in scored]
    output_tps_values = [s["output_tps"] for s in scored]

    # costPriority: lower cost → higher score  (invert)
    cost_scores = _normalise(costs, invert=True)
    # speedPriority: use output_tokens_per_second if any model has it,
    # otherwise a neutral score (no reliable latency proxy is available).
    if any(v > 0 for v in output_tps_values):
        speed_scores = _normalise(output_tps_values, invert=False)
    else:
        speed_scores = [0.5] * len(scored)
    # intelligencePriority: higher max_output → smarter
    intel_scores = _normalise(max_outputs, invert=False)

    best_name = None
    best_score = -1.0
    for i, entry in enumerate(scored):
        score = (
            cost_weight * cost_scores[i]
            + speed_weight * speed_scores[i]
            + intel_weight * intel_scores[i]
        )
        verbose_logger.debug(
            "MCP priority scoring: model=%s cost_score=%.3f speed_score=%.3f "
            "intel_score=%.3f → weighted=%.3f",
            entry["name"],
            cost_scores[i],
            speed_scores[i],
            intel_scores[i],
            score,
        )
        if score > best_score:
            best_score = score
            best_name = entry["name"]

    return best_name

