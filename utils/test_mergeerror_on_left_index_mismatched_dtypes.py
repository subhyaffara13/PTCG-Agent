
def test_mergeerror_on_left_index_mismatched_dtypes():
    # GH 22449
    df_1 = DataFrame(data=["X"], columns=["C"], index=[22])
    df_2 = DataFrame(data=["X"], columns=["C"], index=[999])
    with pytest.raises(MergeError, match="Can only pass argument"):
        merge(df_1, df_2, on=["C"], left_index=True)

