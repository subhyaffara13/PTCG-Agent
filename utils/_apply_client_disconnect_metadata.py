
def _apply_client_disconnect_metadata(target_metadata: dict[str, object]) -> None:
    target_metadata["client_disconnected"] = True
    target_metadata["error_information"] = dict(_CLIENT_DISCONNECTED_ERROR_INFORMATION)

