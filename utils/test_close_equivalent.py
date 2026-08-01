
def test_close_equivalent():
    ''' using a context amanger and using nditer.close are equivalent
    '''
    def add_close(x, y, out=None):
        addop = np.add
        it = np.nditer([x, y, out], [],
                    [['readonly'], ['readonly'], ['writeonly', 'allocate']])
        for (a, b, c) in it:
            addop(a, b, out=c)
        ret = it.operands[2]
        it.close()
        return ret

    def add_context(x, y, out=None):
        addop = np.add
        it = np.nditer([x, y, out], [],
                    [['readonly'], ['readonly'], ['writeonly', 'allocate']])
        with it:
            for (a, b, c) in it:
                addop(a, b, out=c)
            return it.operands[2]
    z = add_close(range(5), range(5))
    assert_equal(z, range(0, 10, 2))
    z = add_context(range(5), range(5))
    assert_equal(z, range(0, 10, 2))

