
def test_svg_incorrect_metadata(metadata, error, message):
    with pytest.raises(error, match=message), BytesIO() as fd:
        fig = plt.figure()
        fig.savefig(fd, format='svg', metadata=metadata)

