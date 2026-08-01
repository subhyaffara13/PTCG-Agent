
def test_concatenate_wrong_type(xp):
    with pytest.raises(TypeError, match='Rotation objects only'):
        rot = Rotation(xp.asarray(Rotation.identity().as_quat()))
        Rotation.concatenate([rot, 1, None])

