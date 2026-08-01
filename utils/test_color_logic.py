
def test_color_logic(pcfunc):
    pcfunc = getattr(plt, pcfunc)
    z = np.arange(12).reshape(3, 4)
    # Explicitly set an edgecolor.
    pc = pcfunc(z, edgecolors='red', facecolors='none')
    pc.update_scalarmappable()  # This is called in draw().
    # Define 2 reference "colors" here for multiple use.
    face_default = mcolors.to_rgba_array(pc._get_default_facecolor())
    mapped = pc.get_cmap()(pc.norm(z.ravel()))
    # GitHub issue #1302:
    assert mcolors.same_color(pc.get_edgecolor(), 'red')
    # Check setting attributes after initialization:
    pc = pcfunc(z)
    pc.set_facecolor('none')
    pc.set_edgecolor('red')
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_facecolor(), 'none')
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    pc.set_alpha(0.5)
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 0.5]])
    pc.set_alpha(None)  # restore default alpha
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    # Reset edgecolor to default.
    pc.set_edgecolor(None)
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_edgecolor(), mapped)
    pc.set_facecolor(None)  # restore default for facecolor
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_facecolor(), mapped)
    assert mcolors.same_color(pc.get_edgecolor(), 'none')
    # Turn off colormapping entirely:
    pc.set_array(None)
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_edgecolor(), 'none')
    assert mcolors.same_color(pc.get_facecolor(), face_default)  # not mapped
    # Turn it back on by restoring the array (must be 1D!):
    pc.set_array(z)
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_facecolor(), mapped)
    assert mcolors.same_color(pc.get_edgecolor(), 'none')
    # Give color via tuple rather than string.
    pc = pcfunc(z, edgecolors=(1, 0, 0), facecolors=(0, 1, 0))
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_facecolor(), mapped)
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    # Provide an RGB array; mapping overrides it.
    pc = pcfunc(z, edgecolors=(1, 0, 0), facecolors=np.ones((12, 3)))
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_facecolor(), mapped)
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    # Turn off the mapping.
    pc.set_array(None)
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_facecolor(), np.ones((12, 3)))
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    # And an RGBA array.
    pc = pcfunc(z, edgecolors=(1, 0, 0), facecolors=np.ones((12, 4)))
    pc.update_scalarmappable()
    assert np.array_equal(pc.get_facecolor(), mapped)
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])
    # Turn off the mapping.
    pc.set_array(None)
    pc.update_scalarmappable()
    assert mcolors.same_color(pc.get_facecolor(), np.ones((12, 4)))
    assert mcolors.same_color(pc.get_edgecolor(), [[1, 0, 0, 1]])

