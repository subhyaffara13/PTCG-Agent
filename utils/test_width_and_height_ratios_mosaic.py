
def test_width_and_height_ratios_mosaic(fig_test, fig_ref,
                                        height_ratios, width_ratios):
    mosaic_spec = [['A', 'B', 'B'], ['A', 'C', 'D']]
    fig_test.subplot_mosaic(mosaic_spec, height_ratios=height_ratios,
                            width_ratios=width_ratios)
    fig_ref.subplot_mosaic(mosaic_spec, gridspec_kw={
                           'height_ratios': height_ratios,
                           'width_ratios': width_ratios})

