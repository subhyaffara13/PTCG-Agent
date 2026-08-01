
def test_labeller():
    """Test the labeller utility"""
    assert labeller(2) == ['q_1', 'q_0']
    assert labeller(3,'j') == ['j_2', 'j_1', 'j_0']

