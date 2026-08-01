
def _gen_invalid_iterdatapipe_msg(datapipe) -> str:
    return (
        "This iterator has been invalidated because another iterator has been created "
        f"from the same IterDataPipe: {_generate_iterdatapipe_msg(datapipe)}\n"
        "This may be caused multiple references to the same IterDataPipe. We recommend "
        "using `.fork()` if that is necessary."
    )

