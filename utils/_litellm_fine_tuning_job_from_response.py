from typing import Any

def _litellm_fine_tuning_job_from_response(
    response: Any, is_azure: bool = False
) -> LiteLLMFineTuningJob:
    return LiteLLMFineTuningJob(
        **_normalize_fine_tuning_job_dict(response.model_dump(), is_azure=is_azure)
    )

