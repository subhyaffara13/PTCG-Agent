from typing import List, Optional

def _key_generation_required_param_check(
    data: GenerateKeyRequest, required_params: Optional[List[str]]
):
    if required_params is None:
        return True

    data_dict = data.model_dump(exclude_unset=True)
    for param in required_params:
        if param not in data_dict:
            raise HTTPException(
                status_code=400,
                detail=f"Required param {param} not in data",
            )
    return True

