
def test_table_cells():
    fig, ax = plt.subplots()
    table = Table(ax)

    cell = table.add_cell(1, 2, 1, 1)
    assert isinstance(cell, CustomCell)
    assert cell is table[1, 2]

    cell2 = CustomCell((0, 0), 1, 2, visible_edges=None)
    table[2, 1] = cell2
    assert table[2, 1] is cell2

    # make sure getitem support has not broken
    # properties and setp
    table.properties()
    plt.setp(table)

