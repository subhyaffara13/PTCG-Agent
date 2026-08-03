from typing import List

def _dedupe_model_candidates(candidates: List[str]) -> List[str]:
    deduped: List[str] = []
    for model in candidates:
        if model not in deduped:
            deduped.append(model)
    return deduped

