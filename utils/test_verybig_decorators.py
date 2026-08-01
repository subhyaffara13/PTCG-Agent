
def test_verybig_decorators(label):
    """Test that no warning emitted when xlabel/ylabel too big."""
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set(**{label: 'a' * 100})

