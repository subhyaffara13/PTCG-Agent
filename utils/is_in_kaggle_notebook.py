
def is_in_kaggle_notebook() -> bool:
    if os.getenv(KAGGLE_NOTEBOOK_ENV_VAR_NAME) is not None:
        if os.getenv(KAGGLE_DATA_PROXY_URL_ENV_VAR_NAME) is None:
            # Missing endpoint for the Jwt client
            get_logger().warning(
                "Can't use the Kaggle Cache. "
                f"The '{KAGGLE_DATA_PROXY_URL_ENV_VAR_NAME}' environment variable is not set."
            )
            return False
        return True
    return False

