
def _create_text_shared_memory(space: Text, n: int = 1, ctx=mp):
    return ctx.Array(np.dtype(np.int32).char, n * space.max_length)

