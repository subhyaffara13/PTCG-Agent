
def configure_artifact_log(log) -> None:
    # If the artifact is off by default, then it should only be logged when explicitly
    # enabled; set propagate to False so that this artifact is not propagated
    # to its ancestor logger
    if log_registry.is_off_by_default(log.artifact_name):
        log.propagate = False

    # enable artifact logging when explicitly enabled
    if log_state.is_artifact_enabled(log.artifact_name):
        log.setLevel(logging.DEBUG)
        log.propagate = True

