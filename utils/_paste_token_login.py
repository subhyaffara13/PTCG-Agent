
def _paste_token_login() -> None:
    logger.info(
        "    To log in, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens ."
    )
    if os.name == "nt":
        logger.info("Token can be pasted using 'Right-Click'.")
    token = getpass("Enter your token (input will not be visible): ")
    _validate_and_save_token(token=token, add_to_git_credential=False)

