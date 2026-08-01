
def test_shared_and_moved():
    # test if sharey is on, but then tick_left is called that labels don't
    # re-appear.  Seaborn does this just to be sure yaxis is on left...
    f, (a1, a2) = plt.subplots(1, 2, sharey=True)
    check_ticklabel_visible([a2], [True], [False])
    a2.yaxis.tick_left()
    check_ticklabel_visible([a2], [True], [False])

    f, (a1, a2) = plt.subplots(2, 1, sharex=True)
    check_ticklabel_visible([a1], [False], [True])
    a2.xaxis.tick_bottom()
    check_ticklabel_visible([a1], [False], [True])

