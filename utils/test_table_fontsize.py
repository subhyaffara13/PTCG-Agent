
def test_table_fontsize():
    # Test that the passed fontsize propagates to cells
    tableData = [['a', 1], ['b', 2]]
    fig, ax = plt.subplots()
    test_fontsize = 20
    t = ax.table(cellText=tableData, loc='top', fontsize=test_fontsize)
    cell_fontsize = t[(0, 0)].get_fontsize()
    assert cell_fontsize == test_fontsize, f"Actual:{test_fontsize},got:{cell_fontsize}"
    cell_fontsize = t[(1, 1)].get_fontsize()
    assert cell_fontsize == test_fontsize, f"Actual:{test_fontsize},got:{cell_fontsize}"

