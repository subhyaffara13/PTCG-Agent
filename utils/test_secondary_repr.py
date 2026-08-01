
def test_secondary_repr():
    fig, ax = plt.subplots()
    secax = ax.secondary_xaxis("top")
    assert repr(secax) == '<SecondaryAxis: >'

