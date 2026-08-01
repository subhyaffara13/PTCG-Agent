
def check_tensor_meta_match(
    t1: torch.Tensor, t2: torch.Tensor, attr_names: tuple[str, ...], msg_prefix: str
) -> None:
    def _get_attr_maybe_call(t: torch.Tensor, attr_name: str) -> Any:
        attr = getattr(t, attr_name)
        if callable(attr):
            return attr()
        return attr

    for attr_name in attr_names:
        lattr = _get_attr_maybe_call(t1, attr_name)
        rattr = _get_attr_maybe_call(t2, attr_name)
        torch._check(
            lattr == rattr,
            lambda: f"{msg_prefix} expected same {attr_name} but got {lattr} and {rattr}.",
        )

