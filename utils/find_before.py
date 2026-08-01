
def find_before(ctx, pos, substr, offsets=(0, 0)):
    new_pos = ctx.source[:pos].rindex(substr)
    return ctx.make_raw_range(new_pos + offsets[0], new_pos + len(substr) + offsets[1])

