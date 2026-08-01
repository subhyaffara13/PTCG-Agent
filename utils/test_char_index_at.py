
def test_char_index_at():
    fig = plt.figure()
    text = fig.text(0.1, 0.9, "")

    text.set_text("i")
    bbox = text.get_window_extent()
    size_i = bbox.x1 - bbox.x0

    text.set_text("m")
    bbox = text.get_window_extent()
    size_m = bbox.x1 - bbox.x0

    text.set_text("iiiimmmm")
    bbox = text.get_window_extent()
    origin = bbox.x0

    assert text._char_index_at(origin - size_i) == 0  # left of first char
    assert text._char_index_at(origin) == 0
    assert text._char_index_at(origin + 0.499*size_i) == 0
    assert text._char_index_at(origin + 0.501*size_i) == 1
    assert text._char_index_at(origin + size_i*3) == 3
    assert text._char_index_at(origin + size_i*4 + size_m*3) == 7
    assert text._char_index_at(origin + size_i*4 + size_m*4) == 8
    assert text._char_index_at(origin + size_i*4 + size_m*10) == 8

