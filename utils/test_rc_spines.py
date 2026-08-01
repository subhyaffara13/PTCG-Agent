
def test_rc_spines():
    rc_dict = {
        'axes.spines.left': False,
        'axes.spines.right': False,
        'axes.spines.top': False,
        'axes.spines.bottom': False}
    with matplotlib.rc_context(rc_dict):
        plt.subplots()  # create a figure and axes with the spine properties

