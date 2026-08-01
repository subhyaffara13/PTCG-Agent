
def check_matching_args(init_sig: FuncSignature, new_sig: FuncSignature) -> bool:
    num_init_args = len(init_sig.args) - init_sig.num_bitmap_args
    num_new_args = len(new_sig.args) - new_sig.num_bitmap_args
    if num_init_args != num_new_args:
        return False

    for idx in range(1, num_init_args):
        init_arg = init_sig.args[idx]
        new_arg = new_sig.args[idx]
        if init_arg.type != new_arg.type:
            return False

        if init_arg.kind != new_arg.kind:
            return False

    return True

