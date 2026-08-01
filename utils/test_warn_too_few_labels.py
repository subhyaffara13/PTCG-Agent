
def test_warn_too_few_labels():
    # note that the axis is still using an AutoLocator:
    fig, ax = plt.subplots()
    with pytest.warns(
           UserWarning,
           match=r'set_ticklabels\(\) should only be used with a fixed number'):
        ax.set_xticklabels(['0', '0.1'])
    # note that the axis is still using a FixedLocator:
    fig, ax = plt.subplots()
    ax.set_xticks([0, 0.5, 1])
    with pytest.raises(ValueError,
                       match='The number of FixedLocator locations'):
        ax.set_xticklabels(['0', '0.1'])

