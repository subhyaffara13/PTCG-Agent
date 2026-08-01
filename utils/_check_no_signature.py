
def _check_no_signature(func) -> None:
    signature = torch.jit.annotations.get_signature(
        func, None, fake_range(), inspect.ismethod(func)
    )
    if signature is None:
        qual_name = _jit_internal._qualified_name(func)
        raise RuntimeError(
            f"Must explicitly add type annotations to overloaded functions: {qual_name}"
        )

