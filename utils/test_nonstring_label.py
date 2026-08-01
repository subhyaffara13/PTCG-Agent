
def test_nonstring_label():
    # Test for #26824
    plt.bar(np.arange(10), np.random.rand(10), label=1)
    plt.legend()

