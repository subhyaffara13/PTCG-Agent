
def _raise_timeout_error(signum, frame):
    raise ValueError(
        "Loading this model requires you to execute custom code contained in the model repository on your local "
        "machine. Please set the option `trust_remote_code=True` to permit loading of this model."
    )

