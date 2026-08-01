
def test_axis_get_tick_params():
    axis = plt.subplot().yaxis
    initial_major_style_translated = {**axis.get_tick_params(which='major')}
    initial_minor_style_translated = {**axis.get_tick_params(which='minor')}

    translated_major_kw = axis._translate_tick_params(
        axis._major_tick_kw, reverse=True
    )
    translated_minor_kw = axis._translate_tick_params(
        axis._minor_tick_kw, reverse=True
    )

    assert translated_major_kw == initial_major_style_translated
    assert translated_minor_kw == initial_minor_style_translated
    axis.set_tick_params(labelsize=30, labelcolor='red',
                         direction='out', which='both')

    new_major_style_translated = {**axis.get_tick_params(which='major')}
    new_minor_style_translated = {**axis.get_tick_params(which='minor')}
    new_major_style = axis._translate_tick_params(new_major_style_translated)
    new_minor_style = axis._translate_tick_params(new_minor_style_translated)
    assert initial_major_style_translated != new_major_style_translated
    assert axis._major_tick_kw == new_major_style
    assert initial_minor_style_translated != new_minor_style_translated
    assert axis._minor_tick_kw == new_minor_style

