
def test_ft2font_face_index(name, size, skippable):
    try:
        file = fm.findfont(name, fallback_to_default=False)
    except ValueError:
        if skippable:
            pytest.skip(r'Font {name} may be missing')
        raise
    for index in range(size):
        font = ft2font.FT2Font(file, face_index=index)
        assert font.num_faces >= size
        assert font.face_index == index
    with pytest.raises(ValueError, match='must be between'):  # out of bounds for spec
        ft2font.FT2Font(file, face_index=0x1ffff)
    with pytest.raises(RuntimeError, match='invalid argument'):  # invalid for this font
        ft2font.FT2Font(file, face_index=0xff)

