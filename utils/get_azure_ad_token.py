
def get_azure_ad_token(
    litellm_params: GenericLiteLLMParams,
) -> Optional[str]:
    """
    Get Azure AD token from various authentication methods.

    This function tries different methods to obtain an Azure AD token:
    1. From an existing token provider
    2. From Entra ID using tenant_id, client_id, and client_secret
    3. From username and password
    4. From OIDC token
    5. From a service principal with secret workflow
    6. From DefaultAzureCredential

    Args:
        litellm_params: Dictionary containing authentication parameters
            - azure_ad_token_provider: Optional callable that returns a token
            - azure_ad_token: Optional existing token
            - tenant_id: Optional Azure tenant ID
            - client_id: Optional Azure client ID
            - client_secret: Optional Azure client secret
            - azure_username: Optional Azure username
            - azure_password: Optional Azure password

    Returns:
        Azure AD token as string if successful, None otherwise
    """
    # Extract parameters
    # Use `or` instead of default parameter to handle cases where key exists but value is None
    azure_ad_token_provider = litellm_params.get("azure_ad_token_provider")
    azure_ad_token = litellm_params.get("azure_ad_token") or get_secret_str(
        "AZURE_AD_TOKEN"
    )
    tenant_id = litellm_params.get("tenant_id") or os.getenv("AZURE_TENANT_ID")
    client_id = litellm_params.get("client_id") or os.getenv("AZURE_CLIENT_ID")
    client_secret = litellm_params.get("client_secret") or os.getenv(
        "AZURE_CLIENT_SECRET"
    )
    azure_username = litellm_params.get("azure_username") or os.getenv("AZURE_USERNAME")
    azure_password = litellm_params.get("azure_password") or os.getenv("AZURE_PASSWORD")
    scope = litellm_params.get("azure_scope") or os.getenv(
        "AZURE_SCOPE", "https://cognitiveservices.azure.com/.default"
    )
    if scope is None:
        scope = "https://cognitiveservices.azure.com/.default"

    # Try to get token provider from Entra ID
    if azure_ad_token_provider is None and tenant_id and client_id and client_secret:
        verbose_logger.debug(
            "Using Azure AD Token Provider from Entra ID for Azure Auth"
        )
        azure_ad_token_provider = get_azure_ad_token_from_entra_id(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )

    # Try to get token provider from username and password
    if (
        azure_ad_token_provider is None
        and azure_username
        and azure_password
        and client_id
    ):
        verbose_logger.debug("Using Azure Username and Password for Azure Auth")
        azure_ad_token_provider = get_azure_ad_token_from_username_password(
            azure_username=azure_username,
            azure_password=azure_password,
            client_id=client_id,
            scope=scope,
        )

    # Try to get token from OIDC
    if (
        client_id
        and tenant_id
        and azure_ad_token
        and azure_ad_token.startswith("oidc/")
    ):
        verbose_logger.debug("Using Azure OIDC Token for Azure Auth")
        azure_ad_token = get_azure_ad_token_from_oidc(
            azure_ad_token=azure_ad_token,
            azure_client_id=client_id,
            azure_tenant_id=tenant_id,
            scope=scope,
        )
    # Try to get token provider from service principal or DefaultAzureCredential
    elif (
        azure_ad_token_provider is None
        and litellm.enable_azure_ad_token_refresh is True
    ):
        verbose_logger.debug(
            "Using Azure AD token provider based on Service Principal with Secret workflow or DefaultAzureCredential for Azure Auth"
        )
        try:
            azure_ad_token_provider = get_azure_ad_token_provider(azure_scope=scope)
        except ValueError:
            verbose_logger.debug("Azure AD Token Provider could not be used.")
        except Exception as e:
            verbose_logger.error(
                f"Error calling Azure AD token provider: {str(e)}. Follow docs - https://docs.litellm.ai/docs/providers/azure/#azure-ad-token-refresh---defaultazurecredential"
            )
            raise e

        #########################################################
        # If litellm.enable_azure_ad_token_refresh is True and no other token provider is available,
        # try to get DefaultAzureCredential provider
        #########################################################
        if azure_ad_token_provider is None and azure_ad_token is None:
            azure_ad_token_provider = (
                BaseAzureLLM._try_get_default_azure_credential_provider(
                    scope=scope,
                )
            )

    # Execute the token provider to get the token if available
    if azure_ad_token_provider and callable(azure_ad_token_provider):
        try:
            token = azure_ad_token_provider()
            if not isinstance(token, str):
                verbose_logger.error(
                    f"Azure AD token provider returned non-string value: {type(token)}"
                )
                raise TypeError(f"Azure AD token must be a string, got {type(token)}")
            else:
                azure_ad_token = token
        except TypeError:
            # Re-raise TypeError directly
            raise
        except Exception as e:
            verbose_logger.error(f"Error calling Azure AD token provider: {str(e)}")
            raise RuntimeError(f"Failed to get Azure AD token: {str(e)}") from e

    return azure_ad_token

