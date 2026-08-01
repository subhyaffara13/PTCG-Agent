
def test_clf_subplotpars():
    keys = ('left', 'right', 'bottom', 'top', 'wspace', 'hspace')
    rc_params = {key: plt.rcParams['figure.subplot.' + key] for key in keys}

    fig = plt.figure(1)
    fig.subplots_adjust(**{k: v+0.01 for k, v in rc_params.items()})
    fig.clf()
    assert fig.subplotpars.to_dict() == rc_params

