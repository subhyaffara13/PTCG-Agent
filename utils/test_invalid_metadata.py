
def test_invalid_metadata():
    fig, ax = plt.subplots()

    with pytest.warns(UserWarning,
                      match="Unknown infodict keyword: 'foobar'."):
        fig.savefig(io.BytesIO(), format='pdf', metadata={'foobar': 'invalid'})

    with pytest.warns(UserWarning,
                      match='not an instance of datetime.datetime.'):
        fig.savefig(io.BytesIO(), format='pdf',
                    metadata={'ModDate': '1968-08-01'})

    with pytest.warns(UserWarning,
                      match='not one of {"True", "False", "Unknown"}'):
        fig.savefig(io.BytesIO(), format='pdf', metadata={'Trapped': 'foo'})

    with pytest.warns(UserWarning, match='not an instance of str.'):
        fig.savefig(io.BytesIO(), format='pdf', metadata={'Title': 1234})

