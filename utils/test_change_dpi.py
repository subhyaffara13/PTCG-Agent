
def test_change_dpi():
    fig = plt.figure(figsize=(4, 4))
    fig.draw_without_rendering()
    assert fig.canvas.renderer.height == 400
    assert fig.canvas.renderer.width == 400
    fig.dpi = 50
    fig.draw_without_rendering()
    assert fig.canvas.renderer.height == 200
    assert fig.canvas.renderer.width == 200

