
def _reset_logs() -> None:
    # reset all registered logs
    for log_qname in log_registry.get_log_qnames():
        log = logging.getLogger(log_qname)
        log.setLevel(logging.WARNING)
        log.propagate = False
        _clear_handlers(log)

    # reset all artifact and child logs
    for artifact_log_qname in itertools.chain(
        log_registry.get_artifact_log_qnames(), log_registry.get_child_log_qnames()
    ):
        log = logging.getLogger(artifact_log_qname)
        log.setLevel(logging.NOTSET)
        log.propagate = True

    trace_log.propagate = False
    _clear_handlers(trace_log)

