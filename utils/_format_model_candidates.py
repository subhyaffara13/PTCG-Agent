from typing import List, Optional, Union

def _format_model_candidates(
    candidates: List[str],
) -> Optional[Union[str, List[str]]]:
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return candidates

