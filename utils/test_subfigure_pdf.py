
def test_subfigure_pdf():
    fig = plt.figure(layout='constrained')
    sub_fig = fig.subfigures()
    ax = sub_fig.add_subplot(111)
    b = ax.bar(1, 1)
    ax.bar_label(b)
    buffer = io.BytesIO()
    fig.savefig(buffer, format='pdf')

