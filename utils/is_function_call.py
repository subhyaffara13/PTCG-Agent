
def is_function_call(optional_params: dict) -> bool:
    """
    Checks if the optional params contain the function call
    """
    if "functions" in optional_params and optional_params.get("functions"):
        return True
    return False

