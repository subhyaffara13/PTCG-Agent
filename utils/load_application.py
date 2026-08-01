
def load_application(data) -> tuple[memoryview, memoryview]:
    """
    U2F application strings
    """
    application, data = _get_sshstr(data)
    if not application.tobytes().startswith(b"ssh:"):
        raise ValueError(
            "U2F application string does not start with b'ssh:' "
            f"({application})"
        )
    return application, data

