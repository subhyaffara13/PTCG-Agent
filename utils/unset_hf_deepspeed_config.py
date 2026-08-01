
def unset_hf_deepspeed_config():
    # useful for unit tests to ensure the global state doesn't leak - call from `tearDown` method
    global _hf_deepspeed_config_weak_ref
    _hf_deepspeed_config_weak_ref = None

