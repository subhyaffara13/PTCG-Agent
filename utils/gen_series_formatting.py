
def gen_series_formatting():
    s1 = Series(["a"] * 100)
    s2 = Series(["ab"] * 100)
    s3 = Series(["a", "ab", "abc", "abcd", "abcde", "abcdef"])
    s4 = s3[::-1]
    test_sers = {"onel": s1, "twol": s2, "asc": s3, "desc": s4}
    return test_sers

