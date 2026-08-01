
def _get_cached_audio_utils():
    """
    Get cached audio_utils.utils module.
    Lazy imports on first call to avoid loading audio_utils.utils at import time.
    Subsequent calls use cached module for better performance.
    """
    global _audio_utils_module
    if _audio_utils_module is None:
        import litellm.litellm_core_utils.audio_utils.utils

        _audio_utils_module = litellm.litellm_core_utils.audio_utils.utils
    return _audio_utils_module

