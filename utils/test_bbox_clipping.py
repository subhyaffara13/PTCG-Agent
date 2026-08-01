
def test_bbox_clipping():
    plt.text(0.9, 0.2, 'Is bbox clipped?', backgroundcolor='r', clip_on=True)
    t = plt.text(0.9, 0.5, 'Is fancy bbox clipped?', clip_on=True)
    t.set_bbox({"boxstyle": "round, pad=0.1"})

