
def test_handler_numpoints():
    """Test legend handler with numpoints <= 1."""
    # related to #6921 and PR #8478
    fig, ax = plt.subplots()
    ax.plot(range(5), label='test')
    ax.legend(numpoints=0.5)

