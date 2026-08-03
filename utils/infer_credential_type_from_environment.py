import os

def infer_credential_type_from_environment() -> AzureCredentialType:
    if (
        os.environ.get("AZURE_CLIENT_ID")
        and os.environ.get("AZURE_CLIENT_SECRET")
        and os.environ.get("AZURE_TENANT_ID")
    ):
        return AzureCredentialType.ClientSecretCredential
    elif os.environ.get("AZURE_CLIENT_ID"):
        return AzureCredentialType.ManagedIdentityCredential
    elif (
        os.environ.get("AZURE_CLIENT_ID")
        and os.environ.get("AZURE_TENANT_ID")
        and os.environ.get("AZURE_CERTIFICATE_PATH")
        and os.environ.get("AZURE_CERTIFICATE_PASSWORD")
    ):
        return AzureCredentialType.CertificateCredential
    elif os.environ.get("AZURE_CERTIFICATE_PASSWORD"):
        return AzureCredentialType.CertificateCredential
    elif os.environ.get("AZURE_CERTIFICATE_PATH"):
        return AzureCredentialType.CertificateCredential
    else:
        return AzureCredentialType.DefaultAzureCredential

