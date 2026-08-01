
def test_cell_with_one_thing_in_it():
    # Regression test - make a cell array that's 1 x 2 and put two
    # strings in it. It works. Make a cell array that's 1 x 1 and put
    # a string in it. It should work but, in the old days, it didn't.
    cells = np.ndarray((1,2),dtype=object)
    cells[0,0] = 'Hello'
    cells[0,1] = 'World'
    savemat(BytesIO(), {'x': cells}, format='5')

    cells = np.ndarray((1,1),dtype=object)
    cells[0,0] = 'Hello, world'
    savemat(BytesIO(), {'x': cells}, format='5')

