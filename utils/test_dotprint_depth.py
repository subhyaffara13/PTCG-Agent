
def test_dotprint_depth():
    text = dotprint(3*x+2, depth=1)
    assert dotnode(3*x+2) in text
    assert dotnode(x) not in text
    text = dotprint(3*x+2)
    assert "depth" not in text

