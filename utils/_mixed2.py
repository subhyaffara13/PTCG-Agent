
def _mixed2(_frame2):
    return DataFrame(
        {
            "A": _frame2["A"],
            "B": _frame2["B"].astype("float32"),
            "C": _frame2["C"].astype("int64"),
            "D": _frame2["D"].astype("int32"),
        }
    )

