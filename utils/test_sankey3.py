
def test_sankey3(fig_test, fig_ref):
    ax_test = fig_test.gca()
    s_test = Sankey(ax=ax_test, flows=[0.25, -0.25, -0.25, 0.25, 0.5, -0.5],
                    orientations=[1, -1, 1, -1, 0, 0])
    s_test.finish()

    ax_ref = fig_ref.gca()
    s_ref = Sankey(ax=ax_ref)
    s_ref.add(flows=[0.25, -0.25, -0.25, 0.25, 0.5, -0.5],
              orientations=[1, -1, 1, -1, 0, 0])
    s_ref.finish()

