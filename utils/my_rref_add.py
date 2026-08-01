
def my_rref_add(rref_t1, t2):
    ret = torch.add(rref_t1.local_value(), t2)
    return ret

