
def is_deepspeed_initialized():
    if is_deepspeed_available():
        return False
    else:
        try:
            import deepspeed

            # This is not available in all DeepSpeed versions.
            return deepspeed.utils.is_initialized()
        except Exception:
            return False

