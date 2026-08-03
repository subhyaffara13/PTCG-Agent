import functools
from typing import Callable

def type_casts(
    f: Callable,
    type_promotion: utils.ELEMENTWISE_TYPE_PROMOTION_KIND,
    compute_dtype_only: bool = False,
    include_non_tensor_args: bool = False,
):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        allowed_types = (
            (Tensor, torch.types._Number) if include_non_tensor_args else (Tensor,)
        )  # type: ignore[arg-type]
        flat_args = [
            x
            for x in pytree.arg_tree_leaves(*args, **kwargs)
            if isinstance(x, allowed_types)
        ]
        computation_dtype, result_dtype = utils.elementwise_dtypes(
            *flat_args, type_promotion_kind=type_promotion
        )

        # TODO: pretty sure this is not quite right
        def increase_prec(x):
            if isinstance(x, Tensor):
                return x.to(computation_dtype)
            else:
                return x

        def decrease_prec(x):
            if isinstance(x, Tensor):
                return x.to(result_dtype)
            else:
                return x

        r = f(*tree_map(increase_prec, args), **tree_map(increase_prec, kwargs))
        if compute_dtype_only:
            return r
        else:
            return tree_map(decrease_prec, r)

    return inner

