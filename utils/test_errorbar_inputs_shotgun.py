
def test_errorbar_inputs_shotgun(kwargs):
    ax = plt.gca()
    eb = ax.errorbar(**kwargs)
    eb.remove()

