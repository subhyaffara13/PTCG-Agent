
def _check_data(xp, rs):
    """
    Check each axes has identical lines

    Parameters
    ----------
    xp : matplotlib Axes object
    rs : matplotlib Axes object
    """
    xp_lines = xp.get_lines()
    rs_lines = rs.get_lines()

    assert len(xp_lines) == len(rs_lines)
    for xpl, rsl in zip(xp_lines, rs_lines, strict=True):
        xpdata = xpl.get_xydata()
        rsdata = rsl.get_xydata()
        tm.assert_almost_equal(xpdata, rsdata)

