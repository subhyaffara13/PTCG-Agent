
def get_api_key_credentials(key):
    """Return credentials with the given API key."""
    from google.auth import api_key

    return api_key.Credentials(key)

