import sys

def load_credentials_from_list(kwargs: dict):
    """
    Updates kwargs with the credentials if credential_name in kwarg
    """
    # Access CredentialAccessor via module to trigger lazy loading if needed
    CredentialAccessor = getattr(sys.modules[__name__], "CredentialAccessor")

    credential_name = kwargs.get("litellm_credential_name")
    if credential_name and litellm.credential_list:
        credential_accessor = CredentialAccessor.get_credential_values(credential_name)
        for key, value in credential_accessor.items():
            if key not in kwargs:
                kwargs[key] = value

