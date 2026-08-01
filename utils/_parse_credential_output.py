
def _parse_credential_output(output: str) -> list[str]:
    """Parse the output of `git credential fill` to extract the password.

    Args:
        output (`str`):
            The output of `git credential fill`.
    """
    # NOTE: If user has set a helper for a custom URL, it will not be caught here.
    #       Example: `credential.https://huggingface.co.helper=store`
    #       See: https://github.com/huggingface/huggingface_hub/pull/1138#discussion_r1013324508
    return sorted(  # Sort for nice printing
        {  # Might have some duplicates
            match[0] for match in GIT_CREDENTIAL_REGEX.findall(output)
        }
    )

