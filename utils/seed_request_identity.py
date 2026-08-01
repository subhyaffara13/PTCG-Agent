
def seed_request_identity(user_api_key_dict: Any, model: Any = None) -> None:
    logger = _registered_v2_logger()
    if logger is not None:
        logger.seed_request_identity(user_api_key_dict, model=model)


def seed_request_identity(user_api_key_dict: Any, model: Any = None) -> None:
    """Seed request-identity Baggage at the auth boundary (no-op without V2)."""
    try:
        from litellm.integrations.otel.logger import (
            seed_request_identity as _seed_request_identity,
        )
    except Exception:
        return
    _seed_request_identity(user_api_key_dict, model=model)

