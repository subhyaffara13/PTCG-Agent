
def contains_tensor_types(type_: Any) -> bool:
    tensor_type = torch._C.TensorType.get()
    return type_.isSubtypeOf(tensor_type) or any(
        contains_tensor_types(e) for e in type_.containedTypes()
    )

