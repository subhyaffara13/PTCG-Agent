from typing import Optional

def _is_async_request(
    kwargs: Optional[dict],
    is_pass_through: bool = False,
) -> bool:
    """
    Returns True if the call type is an internal async request.

    eg. litellm.acompletion, litellm.aimage_generation, litellm.acreate_batch, litellm._arealtime

    Args:
        kwargs (dict): The kwargs passed to the litellm function
        is_pass_through (bool): Whether the call is a pass-through call. By default all pass through calls are async.
    """
    if kwargs is None:
        return False
    if (
        kwargs.get("acompletion", False) is True
        or kwargs.get("aembedding", False) is True
        or kwargs.get("aimg_generation", False) is True
        or kwargs.get("amoderation", False) is True
        or kwargs.get("atext_completion", False) is True
        or kwargs.get("atranscription", False) is True
        or kwargs.get("arerank", False) is True
        or kwargs.get("_arealtime", False) is True
        or kwargs.get("acreate_batch", False) is True
        or kwargs.get("acreate_fine_tuning_job", False) is True
        or is_pass_through is True
    ):
        return True
    return False

