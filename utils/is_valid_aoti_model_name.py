import re

def is_valid_aoti_model_name() -> bool:
    """
    Validates if a model name is suitable for use in code generation.

    """
    from torch._inductor import config

    model_name = config.aot_inductor.model_name_for_generated_files

    if model_name is None:
        return True

    if not isinstance(model_name, str):
        raise ValueError("Invalid AOTI model name: Model name must be a string")

    if model_name == "":
        return True

    # Can only contain alphanumeric characters and underscores
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", model_name):
        raise ValueError(
            "Invalid AOTI model name: Model name can only contain letters, numbers, and underscores"
        )

    return True

