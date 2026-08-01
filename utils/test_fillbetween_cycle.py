
def test_fillbetween_cycle():
    fig, ax = plt.subplots()

    for j in range(3):
        cc = ax.fill_between(range(3), range(3))
        target = mcolors.to_rgba(f'C{j}')
        assert tuple(cc.get_facecolors().squeeze()) == tuple(target)

    for j in range(3, 6):
        cc = ax.fill_betweenx(range(3), range(3))
        target = mcolors.to_rgba(f'C{j}')
        assert tuple(cc.get_facecolors().squeeze()) == tuple(target)

    target = mcolors.to_rgba('k')

    for al in ['facecolor', 'facecolors', 'color']:
        cc = ax.fill_between(range(3), range(3), **{al: 'k'})
        assert tuple(cc.get_facecolors().squeeze()) == tuple(target)

    edge_target = mcolors.to_rgba('k')
    for j, el in enumerate(['edgecolor', 'edgecolors'], start=6):
        cc = ax.fill_between(range(3), range(3), **{el: 'k'})
        face_target = mcolors.to_rgba(f'C{j}')
        assert tuple(cc.get_facecolors().squeeze()) == tuple(face_target)
        assert tuple(cc.get_edgecolors().squeeze()) == tuple(edge_target)

