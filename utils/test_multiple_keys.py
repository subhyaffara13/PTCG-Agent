
def test_multiple_keys():
    # test legend entries with multiple keys
    fig, ax = plt.subplots()
    p1, = ax.plot([1, 2, 3], '-o')
    p2, = ax.plot([2, 3, 4], '-x')
    p3, = ax.plot([3, 4, 5], '-d')
    ax.legend([(p1, p2), (p2, p1), p3], ['two keys', 'pad=0', 'one key'],
              numpoints=1,
              handler_map={(p1, p2): HandlerTuple(ndivide=None),
                           (p2, p1): HandlerTuple(ndivide=None, pad=0)})

