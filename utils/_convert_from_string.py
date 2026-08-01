
def _convert_from_string(data):
    for char in '[]':
        data = data.replace(char, '')

    rows = data.split(';')
    newdata = []
    for count, row in enumerate(rows):
        trow = row.split(',')
        newrow = []
        for col in trow:
            temp = col.split()
            newrow.extend(map(ast.literal_eval, temp))
        if count == 0:
            Ncols = len(newrow)
        elif len(newrow) != Ncols:
            raise ValueError("Rows not the same size.")
        newdata.append(newrow)
    return newdata

