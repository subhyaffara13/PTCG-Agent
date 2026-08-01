
def test_tightlayout_autolayout_deconflict(fig_test, fig_ref):
    for fig, autolayout in zip([fig_ref, fig_test], [False, True]):
        with mpl.rc_context({'figure.autolayout': autolayout}):
            axes = fig.subplots(ncols=2)
            fig.tight_layout(w_pad=10)
        assert isinstance(fig.get_layout_engine(), PlaceHolderLayoutEngine)

