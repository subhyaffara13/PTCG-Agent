
def test_view_preserves_name(index):
    assert index.view().name == index.name

