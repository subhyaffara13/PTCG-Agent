
def test_mat_struct_squeeze():
    stream = BytesIO()
    in_d = {'st':{'one':1, 'two':2}}
    savemat(stream, in_d)
    # no error without squeeze
    loadmat(stream, struct_as_record=False)
    # previous error was with squeeze, with mat_struct
    loadmat(stream, struct_as_record=False, squeeze_me=True)

