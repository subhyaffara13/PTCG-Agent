
def test_various_labels():
    # tests all sorts of label types
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.plot(np.arange(4), 'o', label=1)
    ax.plot(np.linspace(4, 4.1), 'o', label='Développés')
    ax.plot(np.arange(4, 1, -1), 'o', label='__nolegend__')
    ax.legend(numpoints=1, loc='best')

