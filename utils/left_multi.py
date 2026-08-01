
def left_multi():
    return DataFrame(
        {
            "Origin": ["A", "A", "B", "B", "C"],
            "Destination": ["A", "B", "A", "C", "A"],
            "Period": ["AM", "AM", "IP", "AM", "OP"],
            "TripPurp": ["hbw", "nhb", "hbo", "nhb", "hbw"],
            "Trips": [1987, 3647, 2470, 4296, 4444],
        },
        columns=["Origin", "Destination", "Period", "TripPurp", "Trips"],
    ).set_index(["Origin", "Destination", "Period", "TripPurp"])

