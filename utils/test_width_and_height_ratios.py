
def test_width_and_height_ratios(fig_test, fig_ref,
                                 height_ratios, width_ratios):
    fig_test.subplots(2, 3, height_ratios=height_ratios,
                      width_ratios=width_ratios)
    fig_ref.subplots(2, 3, gridspec_kw={
                     'height_ratios': height_ratios,
                     'width_ratios': width_ratios})

