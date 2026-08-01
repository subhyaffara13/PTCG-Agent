
def extract_model_name_from_bedrock_arn(model: str) -> str:
    """
    Extract the model name from an AWS Bedrock ARN.
    Returns the string after the last '/' if 'arn' is in the input string.
    """
    if "arn" in model.lower():
        return model.split("/")[-1]
    return model

