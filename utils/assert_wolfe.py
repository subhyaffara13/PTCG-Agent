
def assert_wolfe(s, phi, derphi, c1=1e-4, c2=0.9, err_msg=""):
    """
    Check that strong Wolfe conditions apply
    """
    phi1 = phi(s)
    phi0 = phi(0)
    derphi0 = derphi(0)
    derphi1 = derphi(s)
    msg = (f"s = {s}; phi(0) = {phi0}; phi(s) = {phi1}; phi'(0) = {derphi0};"
           f" phi'(s) = {derphi1}; {err_msg}")

    assert phi1 <= phi0 + c1*s*derphi0, "Wolfe 1 failed: " + msg
    assert abs(derphi1) <= abs(c2*derphi0), "Wolfe 2 failed: " + msg

