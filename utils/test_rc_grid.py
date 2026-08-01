
def test_rc_grid():
    fig = plt.figure()
    rc_dict0 = {
        'axes.grid': True,
        'axes.grid.axis': 'both'
    }
    rc_dict1 = {
        'axes.grid': True,
        'axes.grid.axis': 'x'
    }
    rc_dict2 = {
        'axes.grid': True,
        'axes.grid.axis': 'y'
    }
    dict_list = [rc_dict0, rc_dict1, rc_dict2]

    for i, rc_dict in enumerate(dict_list, 1):
        with matplotlib.rc_context(rc_dict):
            fig.add_subplot(3, 1, i)

