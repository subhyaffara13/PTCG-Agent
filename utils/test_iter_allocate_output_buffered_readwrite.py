
def test_iter_allocate_output_buffered_readwrite():
    # Allocated output with buffering + delay_bufalloc

    a = arange(6)
    i = nditer([a, None], ['buffered', 'delay_bufalloc'],
                        [['readonly'], ['allocate', 'readwrite']])
    with i:
        i.operands[1][:] = 1
        i.reset()
        for x in i:
            x[1][...] += x[0][...]
        assert_equal(i.operands[1], a + 1)

