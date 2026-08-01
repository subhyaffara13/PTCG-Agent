
def test_generated_op_names(opname, index):
    opname = f"__{opname}__"
    method = getattr(index, opname)
    assert method.__name__ == opname

