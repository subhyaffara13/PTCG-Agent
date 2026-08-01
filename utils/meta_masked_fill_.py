
def meta_masked_fill_(self, mask, value):
    check_inplace_broadcast(self.shape, mask.shape)
    return self

