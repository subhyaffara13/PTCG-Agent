
def test_label_loc_horizontal(fig_test, fig_ref):
    ax = fig_test.subplots()
    sc = ax.scatter([1, 2], [1, 2], c=[1, 2], label='scatter')
    ax.legend()
    ax.set_ylabel('Y Label', loc='bottom')
    ax.set_xlabel('X Label', loc='left')
    cbar = fig_test.colorbar(sc, orientation='horizontal')
    cbar.set_label("Z Label", loc='left')

    ax = fig_ref.subplots()
    sc = ax.scatter([1, 2], [1, 2], c=[1, 2], label='scatter')
    ax.legend()
    ax.set_ylabel('Y Label', y=0, ha='left')
    ax.set_xlabel('X Label', x=0, ha='left')
    cbar = fig_ref.colorbar(sc, orientation='horizontal')
    cbar.set_label("Z Label", x=0, ha='left')

