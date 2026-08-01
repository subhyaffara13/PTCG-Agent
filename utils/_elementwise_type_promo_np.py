
def _elementwise_type_promo_np(*args, type_promotion_kind):
    def _maybe_torch(x):
        if isinstance(x, np.ndarray):
            return torch.from_numpy(x)
        return x

    flattened = pytree.arg_tree_leaves(*args)
    transformed = tuple(_maybe_torch(a) for a in flattened)
    result_dtype, _ = prims.utils.elementwise_dtypes(
        *transformed,
        type_promotion_kind=type_promotion_kind)
    return torch_to_numpy_dtype_dict[result_dtype]

