
def test_shadow_argument_types():
    # Test that different arguments for shadow work as expected
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='test')

    # Test various shadow configurations
    # as well as different ways of specifying colors
    legs = (ax.legend(loc='upper left', shadow=True),    # True
            ax.legend(loc='upper right', shadow=False),  # False
            ax.legend(loc='center left',                 # string
                      shadow={'color': 'red', 'alpha': 0.1}),
            ax.legend(loc='center right',                # tuple
                      shadow={'color': (0.1, 0.2, 0.5), 'oy': -5}),
            ax.legend(loc='lower left',                   # tab
                      shadow={'color': 'tab:cyan', 'ox': 10})
            )
    for l in legs:
        ax.add_artist(l)
    ax.legend(loc='lower right')  # default

