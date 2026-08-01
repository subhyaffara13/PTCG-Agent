
def test_diff_cell_table(text_placeholders):
    cells = ('horizontal', 'vertical', 'open', 'closed', 'T', 'R', 'B', 'L')
    cellText = [['1'] * len(cells)] * 2
    colWidths = [0.1] * len(cells)

    _, axs = plt.subplots(nrows=len(cells), figsize=(4, len(cells)+1), layout='tight')
    for ax, cell in zip(axs, cells):
        ax.table(
                colWidths=colWidths,
                cellText=cellText,
                loc='center',
                edges=cell,
                )
        ax.axis('off')

