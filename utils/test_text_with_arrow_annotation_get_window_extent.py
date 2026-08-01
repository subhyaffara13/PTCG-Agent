
def test_text_with_arrow_annotation_get_window_extent():
    headwidth = 21
    fig, ax = plt.subplots(dpi=100)
    txt = ax.text(s='test', x=0, y=0)
    ann = ax.annotate(
        'test',
        xy=(0.0, 50.0),
        xytext=(50.0, 50.0), xycoords='figure pixels',
        arrowprops={
            'facecolor': 'black', 'width': 2,
            'headwidth': headwidth, 'shrink': 0.0})

    plt.draw()
    renderer = fig.canvas.renderer
    # bounding box of text
    text_bbox = txt.get_window_extent(renderer=renderer)
    # bounding box of annotation (text + arrow)
    bbox = ann.get_window_extent(renderer=renderer)
    # bounding box of arrow
    arrow_bbox = ann.arrow_patch.get_window_extent(renderer)
    # bounding box of annotation text
    ann_txt_bbox = Text.get_window_extent(ann)

    # make sure annotation width is 50 px wider than
    # just the text
    assert bbox.width == text_bbox.width + 50.0
    # make sure the annotation text bounding box is same size
    # as the bounding box of the same string as a Text object
    assert_almost_equal(ann_txt_bbox.height, text_bbox.height)
    assert ann_txt_bbox.width == text_bbox.width
    # compute the expected bounding box of arrow + text
    expected_bbox = mtransforms.Bbox.union([ann_txt_bbox, arrow_bbox])
    assert_almost_equal(bbox.height, expected_bbox.height)

