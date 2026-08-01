
def is_comet_available():
    if _is_comet_installed is False:
        return False

    if _is_comet_recent_enough is False:
        logger.warning(
            "comet_ml version %s is installed, but version %s or higher is required. "
            "Please update comet_ml to the latest version to enable Comet logging with pip install 'comet-ml>=%s'.",
            _comet_version,
            _MIN_COMET_VERSION,
            _MIN_COMET_VERSION,
        )
        return False

    if _is_comet_configured is False:
        logger.warning(
            "comet_ml is installed but the Comet API Key is not configured. "
            "Please set the `COMET_API_KEY` environment variable to enable Comet logging. "
            "Check out the documentation for other ways of configuring it: "
            "https://www.comet.com/docs/v2/guides/experiment-management/configure-sdk/#set-the-api-key"
        )
        return False

    return True

