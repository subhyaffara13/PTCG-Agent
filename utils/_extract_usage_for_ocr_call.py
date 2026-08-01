
def _extract_usage_for_ocr_call(response_obj: Any, response_obj_dict: dict) -> dict:
    """
    Extract usage information for OCR/AOCR calls.

    OCR responses use usage_info (with pages_processed) instead of token-based usage.

    Args:
        response_obj: The raw response object (can be dict, BaseModel, or other)
        response_obj_dict: Dictionary representation of the response object

    Returns:
        A dict with prompt_tokens=0, completion_tokens=0, total_tokens=0,
        and pages_processed from usage_info.
    """
    usage_info = None

    # Try to extract usage_info from dict
    if isinstance(response_obj_dict, dict) and "usage_info" in response_obj_dict:
        usage_info = response_obj_dict.get("usage_info")

    # Try to extract usage_info from object attributes if not found in dict
    if not usage_info and hasattr(response_obj, "usage_info"):
        usage_info = response_obj.usage_info
        if hasattr(usage_info, "model_dump"):
            usage_info = usage_info.model_dump()
        elif hasattr(usage_info, "__dict__"):
            usage_info = vars(usage_info)

    # For OCR, we track pages instead of tokens
    if usage_info is not None:
        # Handle dict or object with attributes
        if isinstance(usage_info, dict):
            result = {
                "prompt_tokens": 0,  # OCR doesn't use traditional tokens
                "completion_tokens": 0,
                "total_tokens": 0,
            }
            # Add all fields from usage_info, including pages_processed
            for key, value in usage_info.items():
                result[key] = value
            # Ensure pages_processed exists
            if "pages_processed" not in result:
                result["pages_processed"] = 0
            return result
        else:
            return {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "pages_processed": 0,
            }
    else:
        return {}

