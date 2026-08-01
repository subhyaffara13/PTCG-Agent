
def test_plot_masked_units():
    data = np.linspace(-5, 5)
    data_masked = np.ma.array(data, mask=(data > -2) & (data < 2))
    data_masked_units = Quantity(data_masked, 'meters')

    fig, ax = plt.subplots()
    ax.plot(data_masked_units)

