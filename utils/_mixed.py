
def _mixed(_frame):
    return DataFrame(
        {
            "A": _frame["A"],
            "B": _frame["B"].astype("float32"),
            "C": _frame["C"].astype("int64"),
            "D": _frame["D"].astype("int32"),
        }
    )

