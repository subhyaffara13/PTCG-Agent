
def test_artist_sublists():
    fig, ax = plt.subplots()
    lines = [ax.plot(np.arange(i, i + 5))[0] for i in range(6)]
    col = ax.scatter(np.arange(5), np.arange(5))
    im = ax.imshow(np.zeros((5, 5)))
    patch = ax.add_patch(mpatches.Rectangle((0, 0), 5, 5))
    text = ax.text(0, 0, 'foo')

    # Get items, which should not be mixed.
    assert list(ax.collections) == [col]
    assert list(ax.images) == [im]
    assert list(ax.lines) == lines
    assert list(ax.patches) == [patch]
    assert not ax.tables
    assert list(ax.texts) == [text]

    # Get items should work like lists/tuple.
    assert ax.lines[0] is lines[0]
    assert ax.lines[-1] is lines[-1]
    with pytest.raises(IndexError, match='out of range'):
        ax.lines[len(lines) + 1]

    # Adding to other lists should produce a regular list.
    assert ax.lines + [1, 2, 3] == [*lines, 1, 2, 3]
    assert [1, 2, 3] + ax.lines == [1, 2, 3, *lines]

    # Adding to other tuples should produce a regular tuples.
    assert ax.lines + (1, 2, 3) == (*lines, 1, 2, 3)
    assert (1, 2, 3) + ax.lines == (1, 2, 3, *lines)

    # Lists should be empty after removing items.
    col.remove()
    assert not ax.collections
    im.remove()
    assert not ax.images
    patch.remove()
    assert not ax.patches
    assert not ax.tables
    text.remove()
    assert not ax.texts

    for ln in ax.lines:
        ln.remove()
    assert len(ax.lines) == 0

