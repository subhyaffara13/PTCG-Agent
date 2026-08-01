
def saved_values(ctx):
    args = []
    t_idx = 0
    s_idx = 0
    saved_tensors = ctx.saved_tensors
    for p in ctx.pos:
        if p == 0:
            args.append(saved_tensors[t_idx])
            t_idx += 1
        else:
            args.append(ctx.non_tensor_args[s_idx])
            s_idx += 1
    if t_idx + s_idx != len(ctx.pos):
        raise AssertionError(
            f"t_idx ({t_idx}) + s_idx ({s_idx}) != len(ctx.pos) ({len(ctx.pos)})"
        )
    return tuple(args)

