
def test_pil_kwargs_webp():
    plt.plot([0, 1, 2], [0, 1, 0])
    buf_small = io.BytesIO()
    pil_kwargs_low = {"quality": 1}
    plt.savefig(buf_small, format="webp", pil_kwargs=pil_kwargs_low)
    assert len(pil_kwargs_low) == 1
    buf_large = io.BytesIO()
    pil_kwargs_high = {"quality": 100}
    plt.savefig(buf_large, format="webp", pil_kwargs=pil_kwargs_high)
    assert len(pil_kwargs_high) == 1
    assert buf_large.getbuffer().nbytes > buf_small.getbuffer().nbytes

