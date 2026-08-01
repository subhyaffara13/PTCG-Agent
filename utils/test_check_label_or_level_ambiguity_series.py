
def test_check_label_or_level_ambiguity_series(df):
    # A series has no columns and therefore references are never ambiguous

    # Make series with L1 as index
    s = df.set_index("L1").L2
    s._check_label_or_level_ambiguity("L1", axis=0)
    s._check_label_or_level_ambiguity("L2", axis=0)

    # Make series with L1 and L2 as index
    s = df.set_index(["L1", "L2"]).L3
    s._check_label_or_level_ambiguity("L1", axis=0)
    s._check_label_or_level_ambiguity("L2", axis=0)
    s._check_label_or_level_ambiguity("L3", axis=0)

