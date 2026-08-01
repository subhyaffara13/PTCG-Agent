
def test_switch_backend_no_close():
    plt.switch_backend('agg')
    fig = plt.figure()
    fig = plt.figure()
    assert len(plt.get_fignums()) == 2
    plt.switch_backend('agg')
    assert len(plt.get_fignums()) == 2
    plt.switch_backend('svg')
    assert len(plt.get_fignums()) == 2

