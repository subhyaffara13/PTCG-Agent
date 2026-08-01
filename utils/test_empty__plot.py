
def test_empty_Plot():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    # No exception showing an empty plot
    plot()
    # Plot is only a base class: doesn't implement any logic for showing
    # images
    p = Plot()
    raises(NotImplementedError, lambda: p.show())

