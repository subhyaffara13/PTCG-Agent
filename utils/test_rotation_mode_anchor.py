
def test_rotation_mode_anchor():
    fig, ax = plt.subplots()

    ax.plot([0, 1], lw=0)
    ax.axvline(.5, linewidth=.5, color='.5')
    ax.axhline(.5, linewidth=.5, color='.5')

    N = 4
    for r in range(N):
        ax.text(.5, .5, 'pP', color=f'C{r}', size=100,
                rotation=r/N*360, rotation_mode='anchor',
                verticalalignment='center_baseline')

