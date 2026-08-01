
def right_multi():
    return DataFrame(
        {
            "Origin": ["A", "A", "B", "B", "C", "C", "E"],
            "Destination": ["A", "B", "A", "B", "A", "B", "F"],
            "Period": ["AM", "AM", "IP", "AM", "OP", "IP", "AM"],
            "LinkType": ["a", "b", "c", "b", "a", "b", "a"],
            "Distance": [100, 80, 90, 80, 75, 35, 55],
        },
        columns=["Origin", "Destination", "Period", "LinkType", "Distance"],
    ).set_index(["Origin", "Destination", "Period", "LinkType"])

