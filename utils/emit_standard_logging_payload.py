
def emit_standard_logging_payload(payload: StandardLoggingPayload):
    if os.getenv("LITELLM_PRINT_STANDARD_LOGGING_PAYLOAD"):
        print(json.dumps(payload, indent=4))  # noqa: T201

