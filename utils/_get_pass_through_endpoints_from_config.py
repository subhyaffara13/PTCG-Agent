from typing import List

def _get_pass_through_endpoints_from_config() -> List[PassThroughGenericEndpoint]:
    """
    Get pass-through endpoints defined in the config file.
    These are read-only and cannot be edited via the UI.
    Malformed endpoints are logged and skipped; they do not crash the function.
    """
    from pydantic import ValidationError

    from litellm.proxy.proxy_server import config_passthrough_endpoints

    if config_passthrough_endpoints is None or len(config_passthrough_endpoints) == 0:
        return []

    returned_endpoints: List[PassThroughGenericEndpoint] = []
    for endpoint in config_passthrough_endpoints:
        try:
            if isinstance(endpoint, dict):
                endpoint_dict = dict(endpoint)
                endpoint_dict["is_from_config"] = True
                returned_endpoints.append(PassThroughGenericEndpoint(**endpoint_dict))
            elif isinstance(endpoint, PassThroughGenericEndpoint):
                # Create a copy with is_from_config=True
                endpoint_dict = endpoint.model_dump()
                endpoint_dict["is_from_config"] = True
                returned_endpoints.append(PassThroughGenericEndpoint(**endpoint_dict))
        except ValidationError as e:
            verbose_proxy_logger.warning(
                "Skipping malformed pass-through endpoint from config: %s",
                e,
                exc_info=False,
            )

    return returned_endpoints

