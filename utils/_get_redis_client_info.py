from typing import List, Tuple

def _get_redis_client_info(cache_instance) -> Tuple[List, int]:
    """
    Helper function to safely get Redis client list information.

    Returns:
        tuple: (client_list, num_clients) where num_clients is -1 if CLIENT LIST is unavailable
    """
    try:
        client_list = cache_instance.client_list()
        return client_list, len(client_list)
    except Exception as e:
        verbose_proxy_logger.warning(
            f"CLIENT LIST command failed (likely restricted on managed Redis): {str(e)}"
        )
        return ["CLIENT LIST command not available on this Redis instance"], -1

