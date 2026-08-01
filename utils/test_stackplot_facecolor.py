
def test_stackplot_facecolor():
    # Test that facecolors are properly passed and take precedence over colors parameter
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1

    facecolors = ['r', 'b']

    fig, ax = plt.subplots()

    colls = ax.stackplot(x, y1, y2, facecolor=facecolors, colors=['c', 'm'])
    for coll, fcolor in zip(colls, facecolors):
        assert mcolors.same_color(coll.get_facecolor(), fcolor)

    # Plural alias should also work
    colls = ax.stackplot(x, y1, y2, facecolors=facecolors, colors=['c', 'm'])
    for coll, fcolor in zip(colls, facecolors):
        assert mcolors.same_color(coll.get_facecolor(), fcolor)

