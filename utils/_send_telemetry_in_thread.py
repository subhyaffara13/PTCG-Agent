
def _send_telemetry_in_thread(
    topic: str,
    *,
    library_name: str | None = None,
    library_version: str | None = None,
    user_agent: dict | str | None = None,
) -> None:
    """Contains the actual data sending data to the Hub.

    This function is called directly in gradio's analytics because
    it is not possible to send telemetry from a daemon thread.

    See here: https://github.com/gradio-app/gradio/pull/8180

    Please do not rename or remove this function.
    """
    path = "/".join(quote(part) for part in topic.split("/") if len(part) > 0)
    try:
        r = get_session().head(
            f"{constants.ENDPOINT}/api/telemetry/{path}",
            headers=build_hf_headers(
                token=False,  # no need to send a token for telemetry
                library_name=library_name,
                library_version=library_version,
                user_agent=user_agent,
            ),
        )
        hf_raise_for_status(r)
    except Exception as e:
        # We don't want to error in case of connection errors of any kind.
        logger.debug(f"Error while sending telemetry: {e}")

