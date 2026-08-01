
def test_process_common_addends():
    # this tests that the args are not evaluated as they are given to do
    # and that key2 works when key1 is False
    do = lambda x: Add(*[i**(i%2) for i in x.args])
    assert process_common_addends(Add(*[1, 2, 3, 4], evaluate=False), do,
        key2=lambda x: x%2, key1=False) == 1**1 + 3**1 + 2**0 + 4**0

