
def safe_unpack_dual(
    dual: torch.Tensor, strict: bool
) -> tuple[torch.Tensor, torch.Tensor]:
    if not isinstance(dual, torch.Tensor):
        raise RuntimeError(
            f"{jvp_str}: expected f(*args) to return only tensors"
            f", got unsupported type {type(dual)}"
        )

    primal, tangent = fwAD.unpack_dual(dual)
    if tangent is None:
        if strict:
            raise RuntimeError(
                "jvp(f, primals, tangents, strict=True): "
                "The output of f is independent of "
                "the inputs. This is not allowed with strict=True."
            )
        tangent = torch.zeros_like(primal)
    return primal, tangent

