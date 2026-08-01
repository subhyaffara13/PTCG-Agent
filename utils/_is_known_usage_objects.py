
def _is_known_usage_objects(usage_obj):
    """Returns True if the usage obj is a known Usage type"""
    return (
        isinstance(usage_obj, litellm.Usage)
        or isinstance(usage_obj, ResponseAPIUsage)
        or TranscriptionUsageObjectTransformation.is_transcription_usage_object(
            usage_obj
        )
    )

