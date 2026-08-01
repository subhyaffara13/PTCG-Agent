
def test_draw_text_as_path_fallback(monkeypatch):
    # Delete RendererAgg.draw_text so that we use the RendererBase.draw_text fallback.
    monkeypatch.delattr('matplotlib.backends.backend_agg.RendererAgg.draw_text')
    heights = [2, 1.5, 3]
    fig = plt.figure(figsize=(6, sum(heights)))
    subfig = fig.subfigures(3, 1, height_ratios=heights)
    _test_complex_shaping(subfig[0])
    _test_text_features(subfig[1])
    _test_text_language(subfig[2])

