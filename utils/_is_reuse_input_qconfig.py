
def _is_reuse_input_qconfig(qconfig: QConfig | None):
    return (
        qconfig is not None
        and isinstance(qconfig.activation(), ReuseInputObserver)
        and isinstance(qconfig.weight(), NoopObserver)
    )

