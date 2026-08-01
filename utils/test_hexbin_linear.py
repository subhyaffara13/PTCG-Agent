
def test_hexbin_linear():
    # Issue #21165
    np.random.seed(19680801)
    n = 100000
    x = np.random.standard_normal(n)
    y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)

    fig, ax = plt.subplots()
    ax.hexbin(x, y, gridsize=(10, 5), marginals=True,
              reduce_C_function=np.sum)

