
def is_from_unspecialized_param_buffer_source(source: Source) -> bool:
    if isinstance(source, UnspecializedParamBufferSource):
        return True
    if isinstance(source, ChainedSource):
        return is_from_unspecialized_param_buffer_source(source.base)
    return False

