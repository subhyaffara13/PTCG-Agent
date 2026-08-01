
def test_text_annotation_get_window_extent():
    figure = Figure(dpi=100)
    renderer = RendererAgg(200, 200, 100)

    # Only text annotation
    annotation = Annotation('test', xy=(0, 0), xycoords='figure pixels')
    annotation.set_figure(figure)

    text = Text(text='test', x=0, y=0)
    text.set_figure(figure)

    bbox = annotation.get_window_extent(renderer=renderer)

    text_bbox = text.get_window_extent(renderer=renderer)
    assert bbox.width == text_bbox.width
    assert bbox.height == text_bbox.height

    _, _, d = renderer.get_text_width_height_descent(
        'text', annotation._fontproperties, ismath=False)
    font = get_font(fontManager._find_fonts_by_props(annotation._fontproperties))
    for name, key in [('OS/2', 'sTypoDescender'), ('hhea', 'descent')]:
        if (table := font.get_sfnt_table(name)) is not None:
            units_per_em = font.get_sfnt_table('head')['unitsPerEm']
            fontsize = annotation._fontproperties.get_size_in_points()
            lp_d = -table[key] / units_per_em * fontsize * figure.dpi / 72
            break
    else:
        _, _, lp_d = renderer.get_text_width_height_descent(
            'lp', annotation._fontproperties, ismath=False)
    below_line = max(d, lp_d)

    # These numbers are specific to the current implementation of Text
    points = bbox.get_points()
    assert points[0, 0] == 0.0
    assert points[1, 0] == text_bbox.width
    assert points[0, 1] == -below_line
    assert points[1, 1] == text_bbox.height - below_line

