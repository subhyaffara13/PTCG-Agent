
def test_text_repr():
    # smoketest to make sure text repr doesn't error for category
    plt.plot(['A', 'B'], [1, 2])
    repr(plt.text(['A'], 0.5, 'Boo'))

