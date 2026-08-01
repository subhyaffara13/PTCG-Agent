
def test_apply_concat_preserve_names(three_group):
    grouped = three_group.groupby(["A", "B"])

    def desc(group):
        result = group.describe()
        result.index.name = "stat"
        return result

    def desc2(group):
        result = group.describe()
        result.index.name = "stat"
        result = result[: len(group)]
        # weirdo
        return result

    def desc3(group):
        result = group.describe()

        # names are different
        result.index.name = f"stat_{len(group):d}"

        result = result[: len(group)]
        # weirdo
        return result

    result = grouped.apply(desc)
    assert result.index.names == ("A", "B", "stat")

    result2 = grouped.apply(desc2)
    assert result2.index.names == ("A", "B", "stat")

    result3 = grouped.apply(desc3)
    assert result3.index.names == ("A", "B", None)

