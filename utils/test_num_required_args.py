
def test_num_required_args():
    assert num_required_args(lambda: None) == 0
    assert num_required_args(lambda x: None) == 1
    assert num_required_args(lambda x, *args: None) == 1
    assert num_required_args(lambda x, **kwargs: None) == 1
    assert num_required_args(lambda x, y, *args, **kwargs: None) == 2
    assert num_required_args(map) == 2
    assert num_required_args(dict) is None

