
def _get_model_info(func, parent_class):
    """
    Extract model information from a function or its parent class.

    Args:
        func (`function`): The function to extract information from
        parent_class (`class`): Optional parent class of the function
    """
    # import here to avoid circular import
    from transformers.models import auto as auto_module

    # Get model name from either parent class or function
    if parent_class is not None:
        model_name_lowercase = get_model_name(parent_class)
    else:
        model_name_lowercase = get_model_name(func)

    # Normalize model name if needed
    if model_name_lowercase and model_name_lowercase not in getattr(
        getattr(auto_module, PLACEHOLDER_TO_AUTO_MODULE["config_class"][0]),
        PLACEHOLDER_TO_AUTO_MODULE["config_class"][1],
    ):
        model_name_lowercase = model_name_lowercase.replace("_", "-")

    # Get class name from function's qualified name
    class_name = func.__qualname__.split(".")[0]

    # Get config class for the model
    if model_name_lowercase is None:
        config_class = None
    else:
        try:
            config_class = getattr(
                getattr(auto_module, PLACEHOLDER_TO_AUTO_MODULE["config_class"][0]),
                PLACEHOLDER_TO_AUTO_MODULE["config_class"][1],
            )[model_name_lowercase]
        except KeyError:
            if model_name_lowercase in HARDCODED_CONFIG_FOR_MODELS:
                config_class = HARDCODED_CONFIG_FOR_MODELS[model_name_lowercase]
            else:
                config_class = "ModelConfig"
                print(
                    f"[ERROR] Config not found for {model_name_lowercase}. You can manually add it to HARDCODED_CONFIG_FOR_MODELS in utils/auto_docstring.py"
                )
    return model_name_lowercase, class_name, config_class

