import os

def _environment_bearer_token() -> str:
    token = os.environ.get("AWS_BEARER_TOKEN_BEDROCK")
    if not token:
        raise OpenAIError(
            "Could not find credentials for Bedrock. Set `AWS_BEARER_TOKEN_BEDROCK` or configure the default "
            "AWS credential chain."
        )
    return token

