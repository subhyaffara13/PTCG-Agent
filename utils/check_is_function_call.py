
def check_is_function_call(logging_obj: "LoggingClass") -> bool:
    from litellm.litellm_core_utils.prompt_templates.common_utils import (
        is_function_call,
    )

    if hasattr(logging_obj, "optional_params") and isinstance(
        logging_obj.optional_params, dict
    ):
        if is_function_call(logging_obj.optional_params):
            return True

    return False

