
def test_only_on_non_finite_bbox():
    fig, ax = plt.subplots()
    ax.annotate("", xy=(0, float('nan')))
    ax.set_axis_off()
    # we only need to test that it does not error out on save
    fig.savefig(BytesIO(), bbox_inches='tight', format='png')

