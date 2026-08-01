
def test_universal_newlines_quoted(newline):
    # Check that universal newline support within the tokenizer is not applied
    # to quoted fields.  (note that lines must end in newline or quoted
    # fields will not include a newline at all)
    data = ['1,"2\n"\n', '3,"4\n', '1"\n']
    data = [row.replace("\n", newline) for row in data]
    res = np.loadtxt(data, dtype=object, delimiter=",", quotechar='"')
    assert_array_equal(res, [['1', f'2{newline}'], ['3', f'4{newline}1']])

