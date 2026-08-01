
def test_rcparams_reset_after_fail():
    # There was previously a bug that meant that if rc_context failed and
    # raised an exception due to issues in the supplied rc parameters, the
    # global rc parameters were left in a modified state.
    with mpl.rc_context(rc={'text.usetex': False}):
        assert mpl.rcParams['text.usetex'] is False
        with pytest.raises(KeyError):
            with mpl.rc_context(rc={'text.usetex': True, 'test.blah': True}):
                pass
        assert mpl.rcParams['text.usetex'] is False

