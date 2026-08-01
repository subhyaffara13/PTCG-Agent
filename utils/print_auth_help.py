
def print_auth_help() -> None:
    """Print friendly instructions for setting up Kaggle authentication."""
    print(
        "Authentication required to call the Kaggle API.\n"
        "\n"
        "First, you will need a Kaggle account. You can sign up at\n"
        "  https://www.kaggle.com/account/login\n"
        "\n"
        "Recommended: log in with OAuth via a web-based authorization flow.\n"
        "No token to manage; credentials are cached locally for you.\n"
        "    kaggle auth login\n"
        "\n"
        "If you'd rather not use OAuth, generate an API token at\n"
        '  https://www.kaggle.com/settings/api  (click "Generate New Token" under "API")\n'
        "and supply it to the CLI in one of these ways:\n"
        "\n"
        "  Option A: Environment variable\n"
        "    export KAGGLE_API_TOKEN=xxxxxxxxxxxxxx  # token copied from the settings UI\n"
        "\n"
        "  Option B: API token file\n"
        "    Save the token to ~/.kaggle/access_token"
    )

