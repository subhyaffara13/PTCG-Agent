
def _all_gather_into_tensor_coalesced_meta(self, tag, rankset, group_size):
    return [_make_all_gather_out_tensor(t, group_size) for t in self]

