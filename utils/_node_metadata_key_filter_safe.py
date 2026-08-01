
def _node_metadata_key_filter_safe(key: str) -> bool:
    """
    A metadata filter which allows pickle-safe node metadata. These often times contain
    stacks with pointers to unserializable objects, so we clear them out.
    """
    return key not in ["source_fn_stack", "nn_module_stack", "fwd_source_fn_stack"]

