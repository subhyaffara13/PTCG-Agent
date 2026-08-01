
def are_all_mutations_under_no_grad_or_inference_mode(t: torch.Tensor) -> bool:
    if is_traceable_wrapper_subclass(t):
        attrs, _ = t.__tensor_flatten__()
        for attr in attrs:
            match getattr(t, attr):
                case Tensor() as v:
                    if not are_all_mutations_under_no_grad_or_inference_mode(v):
                        return False
                case OpaqueBase():
                    pass
                case unexpected:
                    raise AssertionError(
                        f"expected Tensor or OpaqueBase, got {type(unexpected)}"
                    )
        return True
    else:
        if not isinstance(t, FunctionalTensor):
            raise AssertionError(f"expected FunctionalTensor, got {type(t)}")
        return torch._functionalize_are_all_mutations_under_no_grad_or_inference_mode(
            t.elem
        )

