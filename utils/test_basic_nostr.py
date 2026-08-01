
def test_basic_nostr():
    for obj in basic_objs:
        raises(TypeError, lambda: obj + '1')
        raises(TypeError, lambda: obj - '1')
        if obj == 2:
            assert obj * '1' == '11'
        else:
            raises(TypeError, lambda: obj * '1')
        raises(TypeError, lambda: obj / '1')
        raises(TypeError, lambda: obj ** '1')

