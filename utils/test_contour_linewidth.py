
def test_contour_linewidth(
        rc_lines_linewidth, rc_contour_linewidth, call_linewidths, expected):

    with rc_context(rc={"lines.linewidth": rc_lines_linewidth,
                        "contour.linewidth": rc_contour_linewidth}):
        fig, ax = plt.subplots()
        X = np.arange(4*3).reshape(4, 3)
        cs = ax.contour(X, linewidths=call_linewidths)
        assert cs.get_linewidths()[0] == expected

