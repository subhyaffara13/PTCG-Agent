
def test_kane_rolling_disc_lu():
    props = _create_rolling_disc()
    kane = KanesMethod(props['frame'], props['q_ind'], props['u_ind'],
                       props['kdes'], u_dependent=props['u_dep'],
                       velocity_constraints=props['fnh'],
                       bodies=props['bodies'], forcelist=props['loads'],
                       explicit_kinematics=False, constraint_solver='LU')
    kane.kanes_equations()
    _verify_rolling_disc_numerically(kane)

