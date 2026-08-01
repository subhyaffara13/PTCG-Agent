
def _get_bearer_token_or_received_api_key(api_key: str) -> str:
    if api_key.startswith("Bearer "):  # ensure Bearer token passed in
        api_key = api_key.replace("Bearer ", "")  # extract the token
    elif api_key.startswith("Basic "):
        api_key = api_key.replace("Basic ", "")  # handle langfuse input
    elif api_key.startswith("bearer "):
        api_key = api_key.replace("bearer ", "")
    elif api_key.startswith("AWS4-HMAC-SHA256"):
        # Handle AWS Signature V4 format from LangChain
        # Format: AWS4-HMAC-SHA256 Credential=Bearer sk-12345/date/region/service/aws4_request, SignedHeaders=..., Signature=...
        # Extract the Bearer token from the Credential field
        match = re.search(r"Credential=Bearer\s+([^/\s,]+)", api_key)
        if match:
            api_key = match.group(1)
        else:
            # If no Bearer token found in Credential, try to extract just the credential value
            match = re.search(r"Credential=([^/\s,]+)", api_key)
            if match:
                api_key = match.group(1)

    return api_key

