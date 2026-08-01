
def test_too_large_image():
    fig = plt.figure(figsize=(300, 2**25))
    buff = io.BytesIO()
    with pytest.raises(ValueError):
        fig.savefig(buff)

