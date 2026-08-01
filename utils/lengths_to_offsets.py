
def lengths_to_offsets(t, offset_type=np.int64, use_begin_offset=True):
    """
    Convert lengths to offsets for embedding_bag
    """
    tt = np.zeros((t.shape[0] + 1,), dtype=offset_type)
    tt[1:] = t
    tt = torch.from_numpy(np.cumsum(tt, dtype=offset_type))
    if use_begin_offset:
        return tt[:-1]
    return tt[1:]

