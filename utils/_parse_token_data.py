import json

def _parse_token_data(token_content, format_type="text", subject_token_field_name=None):
    if format_type == "text":
        token = token_content.content
    else:
        try:
            # Parse file content as JSON.
            response_data = json.loads(token_content.content)
            # Get the subject_token.
            token = response_data[subject_token_field_name]
        except (KeyError, ValueError):
            raise exceptions.RefreshError(
                "Unable to parse subject_token from JSON file '{}' using key '{}'".format(
                    token_content.location, subject_token_field_name
                )
            )
    if not token:
        raise exceptions.RefreshError(
            "Missing subject_token in the credential_source file"
        )
    return token

