
def test_np_matmul():
    # GH26650
    df1 = pd.DataFrame(data=[[-1, 1, 10]])
    df2 = pd.DataFrame(data=[-1, 1, 10])
    expected = pd.DataFrame(data=[102])

    result = np.matmul(df1, df2)
    tm.assert_frame_equal(expected, result)

