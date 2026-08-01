
def _check_has_fake_tensor(node: torch.fx.Node) -> None:
    # TODO(angelayi): remove this in favor of _check_val
    return _check_val(node)

