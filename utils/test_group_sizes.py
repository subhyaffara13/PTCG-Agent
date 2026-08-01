
def test_group_sizes(name, size):
    assert len(Rotation.create_group(name)) == size

