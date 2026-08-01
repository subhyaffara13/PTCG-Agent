
def assert_armijo(s, phi, c1=1e-4, err_msg=""):
    """
    Check that Armijo condition applies
    """
    phi1 = phi(s)
    phi0 = phi(0)
    msg = f"s = {s}; phi(0) = {phi0}; phi(s) = {phi1}; {err_msg}"
    assert phi1 <= (1 - c1*s)*phi0, msg

