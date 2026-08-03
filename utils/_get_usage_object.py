from typing import Any, Optional, Union

def _get_usage_object(
    completion_response: Any,
) -> Optional[Usage]:
    usage_obj = cast(
        Union[Usage, ResponseAPIUsage, dict, BaseModel],
        (
            completion_response.get("usage")
            if isinstance(completion_response, dict)
            else getattr(completion_response, "get", lambda x: None)("usage")
        ),
    )

    if usage_obj is None:
        return None
    if isinstance(usage_obj, Usage):
        return usage_obj
    elif (
        usage_obj is not None
        and (isinstance(usage_obj, dict) or isinstance(usage_obj, ResponseAPIUsage))
        and ResponseAPILoggingUtils._is_response_api_usage(usage_obj)
    ):
        return ResponseAPILoggingUtils._transform_response_api_usage_to_chat_usage(
            usage_obj
        )
    elif TranscriptionUsageObjectTransformation.is_transcription_usage_object(
        usage_obj
    ):
        return (
            TranscriptionUsageObjectTransformation.transform_transcription_usage_object(
                cast(
                    Union[
                        TranscriptionUsageDurationObject, TranscriptionUsageTokensObject
                    ],
                    usage_obj,
                )
            )
        )
    elif isinstance(usage_obj, dict):
        return Usage(**usage_obj)
    elif isinstance(usage_obj, BaseModel):
        return Usage(**usage_obj.model_dump())
    else:
        verbose_logger.debug(
            f"Unknown usage object type: {type(usage_obj)}, usage_obj: {usage_obj}"
        )
        return None

