
def get_const_index(code_options: dict[str, Any], val: Any) -> int:
    for i, v in enumerate(code_options["co_consts"]):
        # NOTE: stronger comparison is required, since we have
        # examples where two values compare equal but have
        # different semantic meaning in some cases, e.g.
        # 0.0 == -0.0 but have different effects in torch.copysign.
        if val is v:
            return i
    code_options["co_consts"] += (val,)
    return len(code_options["co_consts"]) - 1

