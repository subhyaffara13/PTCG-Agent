
def check_model_inputs(func):
    logger.warning_once("The `check_model_inputs` decorator is deprecated in favor of `merge_with_config_defaults`.")
    return merge_with_config_defaults(func)

