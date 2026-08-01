
def test_kwargs_pass():
    fig = Figure(label='whole Figure')
    sub_fig = fig.subfigures(1, 1, label='sub figure')

    assert fig.get_label() == 'whole Figure'
    assert sub_fig.get_label() == 'sub figure'

