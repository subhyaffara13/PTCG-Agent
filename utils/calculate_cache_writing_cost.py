from typing import Optional

def calculate_cache_writing_cost(
    cache_creation_tokens: int,
    cache_creation_token_details: Optional[CacheCreationTokenDetails],
    cache_creation_cost_above_1hr: float,
    cache_creation_cost: float,
) -> float:
    """
    Adjust cost of cache creation tokens based on the cache creation token details.
    """
    total_cost: float = 0.0
    if cache_creation_token_details is not None:
        # get the number of 5m and 1h cache creation tokens
        cache_creation_tokens_5m = (
            cache_creation_token_details.ephemeral_5m_input_tokens
        )
        cache_creation_tokens_1h = (
            cache_creation_token_details.ephemeral_1h_input_tokens
        )
        # add the number of 5m and 1h cache creation tokens to the cache creation tokens
        total_cost += (
            cache_creation_tokens_5m * cache_creation_cost
            if cache_creation_tokens_5m is not None
            else 0.0
        )
        total_cost += (
            cache_creation_tokens_1h * cache_creation_cost_above_1hr
            if cache_creation_tokens_1h is not None
            else 0.0
        )
    else:
        total_cost += cache_creation_tokens * cache_creation_cost
    return total_cost

