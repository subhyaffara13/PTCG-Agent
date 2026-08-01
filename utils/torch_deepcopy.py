
def torch_deepcopy(value):
    if isinstance(value, (int, float, str)):
        return value
    if isinstance(value, tuple):
        return tuple(torch_deepcopy(v) for v in value)
    if isinstance(value, list):
        return [torch_deepcopy(v) for v in value]
    if isinstance(value, set):
        return {torch_deepcopy(v) for v in value}
    if isinstance(value, dict):
        return {k: torch_deepcopy(v) for k, v in value.items()}
    if isinstance(value, np.ndarray):
        return value.copy()
    if hasattr(value, "clone"):
        return value.clone()
    if isinstance(value, DynamicCache):
        return make_dynamic_cache(torch_deepcopy(list(zip(value.key_cache, value.value_cache, strict=False))))
    # We should have a code using serialization, deserialization assuming a model
    # cannot be exported without them.
    raise NotImplementedError(f"torch_deepcopy not implemented for type {type(value)}")

