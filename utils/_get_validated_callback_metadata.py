from typing import Optional

def _get_validated_callback_metadata(
    item: dict, *, source: str
) -> Optional[AddTeamCallback]:
    try:
        return AddTeamCallback(**item)
    except (PydanticValidationError, ValueError) as e:
        verbose_proxy_logger.warning(
            "Ignoring invalid %s callback metadata: %s",
            source,
            _sanitize_for_log(str(e)),
        )
        return None

