import os

def get_current_validator():
    """
    Return the default validator based on the value of an environment variable.
    """
    validator_name = os.environ.get("NBFORMAT_VALIDATOR", "fastjsonschema")
    return _validator_for_name(validator_name)

