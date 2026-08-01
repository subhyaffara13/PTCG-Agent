
def test_suptitle_subfigures():
    fig = plt.figure(figsize=(4, 3))
    sf1, sf2 = fig.subfigures(1, 2)
    sf2.set_facecolor('white')
    sf1.subplots()
    sf2.subplots()
    fig.suptitle("This is a visible suptitle.")

    # verify the first subfigure facecolor is the default transparent
    assert sf1.get_facecolor() == (0.0, 0.0, 0.0, 0.0)
    # verify the second subfigure facecolor is white
    assert sf2.get_facecolor() == (1.0, 1.0, 1.0, 1.0)

