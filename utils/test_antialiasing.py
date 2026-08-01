
def test_antialiasing():
    mpl.rcParams['text.antialiased'] = False  # Passed arguments should override.

    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.3, 0.75, "antialiased", horizontalalignment='center',
             verticalalignment='center', antialiased=True)
    fig.text(0.3, 0.25, r"$\sqrt{x}$", horizontalalignment='center',
             verticalalignment='center', antialiased=True)

    mpl.rcParams['text.antialiased'] = True  # Passed arguments should override.
    fig.text(0.7, 0.75, "not antialiased", horizontalalignment='center',
             verticalalignment='center', antialiased=False)
    fig.text(0.7, 0.25, r"$\sqrt{x}$", horizontalalignment='center',
             verticalalignment='center', antialiased=False)

    mpl.rcParams['text.antialiased'] = False  # Should not affect existing text.

