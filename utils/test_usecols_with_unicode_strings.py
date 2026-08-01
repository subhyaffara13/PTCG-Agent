
def test_usecols_with_unicode_strings(all_parsers):
    # see gh-13219
    data = """AAA,BBB,CCC,DDD
0.056674973,8,True,a
2.613230982,2,False,b
3.568935038,7,False,a"""
    parser = all_parsers

    exp_data = {
        "AAA": {
            0: 0.056674972999999997,
            1: 2.6132309819999997,
            2: 3.5689350380000002,
        },
        "BBB": {0: 8, 1: 2, 2: 7},
    }
    expected = DataFrame(exp_data)

    result = parser.read_csv(StringIO(data), usecols=["AAA", "BBB"])
    tm.assert_frame_equal(result, expected)

