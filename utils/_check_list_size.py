
def _check_list_size(out_len: int, get_infos: bool, out: _ListOrSeq) -> None:
    get_infos_int = 1 if get_infos else 0
    if out_len - get_infos_int != 2:
        raise TypeError(
            f"expected tuple of {2 + int(get_infos)} elements but got {out_len}"
        )
    if not isinstance(out, (tuple, list)):
        raise TypeError(
            f"argument 'out' must be tuple of Tensors, not {type(out).__name__}"
        )

