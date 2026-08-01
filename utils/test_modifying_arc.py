
def test_modifying_arc(fig_test, fig_ref):
    arc1 = Arc([.5, .5], .5, 1, theta1=0, theta2=60, angle=20)
    arc2 = Arc([.5, .5], 1.5, 1, theta1=0, theta2=60, angle=10)
    fig_ref.subplots().add_patch(arc1)
    fig_test.subplots().add_patch(arc2)
    arc2.set_width(.5)
    arc2.set_angle(20)

