
def test_legend_generator():
    # smoketest that generator inputs work
    fig, ax = plt.subplots()
    ax.plot([0, 1])
    ax.plot([0, 2])

    handles = (line for line in ax.get_lines())
    labels = (label for label in ['spam', 'eggs'])

    ax.legend(handles, labels, loc='upper left')

