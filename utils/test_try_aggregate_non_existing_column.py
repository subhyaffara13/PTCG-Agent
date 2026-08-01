
def test_try_aggregate_non_existing_column():
    # GH 16766
    data = [
        {"dt": datetime(2017, 6, 1, 0), "x": 1.0, "y": 2.0},
        {"dt": datetime(2017, 6, 1, 1), "x": 2.0, "y": 2.0},
        {"dt": datetime(2017, 6, 1, 2), "x": 3.0, "y": 1.5},
    ]
    df = DataFrame(data).set_index("dt")

    # Error as we don't have 'z' column
    msg = r"Label\(s\) \['z'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        df.resample("30min").agg({"x": ["mean"], "y": ["median"], "z": ["sum"]})

