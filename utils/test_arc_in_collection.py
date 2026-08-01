
def test_arc_in_collection(fig_test, fig_ref):
    arc1 = Arc([.5, .5], .5, 1, theta1=0, theta2=60, angle=20)
    arc2 = Arc([.5, .5], .5, 1, theta1=0, theta2=60, angle=20)
    col = mcollections.PatchCollection(patches=[arc2], facecolors='none',
                                       edgecolors='k')
    ax_ref = fig_ref.subplots()
    ax_ref.add_patch(arc1)
    ax_ref.autoscale_view()
    fig_test.subplots().add_collection(col)

