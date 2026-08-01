
def copy_dynamo_tensor_attributes(src: torch.Tensor, dst: torch.Tensor) -> None:
    """
    Copy dynamo-specific tensor attributes from src to dst.
    These attributes are used for dynamic shape marking and must be preserved
    when cloning or casting tensors. If src doesn't have an attribute but dst does,
    the attribute is removed from dst.
    """
    _copy_dynamo_attr(src, dst, "_dynamo_dynamic_indices")
    _copy_dynamo_attr(src, dst, "_dynamo_unbacked_indices")
    _copy_dynamo_attr(src, dst, "_dynamo_hint_overrides")
    _copy_dynamo_attr(src, dst, "_dynamo_shape_ids")
    _copy_dynamo_attr(src, dst, "_dynamo_strict_unbacked_indices")
    _copy_dynamo_attr(src, dst, "_dynamo_weak_dynamic_indices")

