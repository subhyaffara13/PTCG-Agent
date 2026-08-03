from typing import List, Optional

def should_use_cohere_v1_client(
    api_base: Optional[str], present_version_params: List[str]
):
    if not api_base:
        return False
    uses_v1_params = ("max_chunks_per_doc" in present_version_params) and (
        "max_tokens_per_doc" not in present_version_params
    )
    return api_base.endswith("/v1/rerank") or (
        uses_v1_params and not api_base.endswith("/v2/rerank")
    )

