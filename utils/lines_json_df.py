
def lines_json_df():
    df = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    return df.to_json(lines=True, orient="records")

