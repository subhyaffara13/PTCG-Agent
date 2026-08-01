
def test_fignum_exists():
    # pyplot figure creation, selection and closing with fignum_exists
    plt.figure('one')
    plt.figure(2)
    plt.figure('three')
    plt.figure()
    assert plt.fignum_exists('one')
    assert plt.fignum_exists(2)
    assert plt.fignum_exists('three')
    assert plt.fignum_exists(4)
    plt.close('one')
    plt.close(4)
    assert not plt.fignum_exists('one')
    assert not plt.fignum_exists(4)

