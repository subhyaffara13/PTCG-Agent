import logging

def getArtifactLogger(module_qname, artifact_name) -> logging.Logger:
    if artifact_name not in log_registry.artifact_names:
        raise ValueError(
            f"Artifact name: {repr(artifact_name)} not registered,"
            f"please call register_artifact({repr(artifact_name)}) in torch._logging.registrations."
        )
    qname = module_qname + f".__{artifact_name}"
    log = logging.getLogger(qname)
    log.artifact_name = artifact_name  # type: ignore[attr-defined]
    log_registry.register_artifact_log(qname)
    configure_artifact_log(log)
    return log

