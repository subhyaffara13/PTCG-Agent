
def test_set_group_name(df, grouper):
    def f(group):
        assert group.name is not None
        return group

    def freduce(group):
        assert group.name is not None
        return group.sum()

    def freducex(x):
        return freduce(x)

    grouped = df.groupby(grouper, group_keys=False)

    # make sure all these work
    grouped.apply(f)
    grouped.aggregate(freduce)
    grouped.aggregate({"C": freduce, "D": freduce})
    grouped.transform(f)

    grouped["C"].apply(f)
    grouped["C"].aggregate(freduce)
    grouped["C"].aggregate([freduce, freducex])
    grouped["C"].transform(f)

