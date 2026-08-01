
def test_large_subscript_title():
    plt.rcParams['axes.titley'] = None

    fig, axs = plt.subplots(1, 2, figsize=(9, 2.5), constrained_layout=True)
    ax = axs[0]
    ax.set_title(r'$\sum_{i} x_i$')
    ax.set_title('New way', loc='left')
    ax.set_xticklabels([])

    ax = axs[1]
    ax.set_title(r'$\sum_{i} x_i$', y=1.01)
    ax.set_title('Old Way', loc='left')
    ax.set_xticklabels([])

