
def leap_second(test):
    message = "Leap seconds are unsupported."
    return skip(
        message=message,
        subject="time",
        description="a valid time string with leap second",
    )(test) or skip(
        message=message,
        subject="time",
        description="a valid time string with leap second, Zulu",
    )(test) or skip(
        message=message,
        subject="time",
        description="a valid time string with leap second with offset",
    )(test) or skip(
        message=message,
        subject="time",
        description="valid leap second, positive time-offset",
    )(test) or skip(
        message=message,
        subject="time",
        description="valid leap second, negative time-offset",
    )(test) or skip(
        message=message,
        subject="time",
        description="valid leap second, large positive time-offset",
    )(test) or skip(
        message=message,
        subject="time",
        description="valid leap second, large negative time-offset",
    )(test) or skip(
        message=message,
        subject="time",
        description="valid leap second, zero time-offset",
    )(test) or skip(
        message=message,
        subject="date-time",
        description="a valid date-time with a leap second, UTC",
    )(test) or skip(
        message=message,
        subject="date-time",
        description="a valid date-time with a leap second, with minus offset",
    )(test)

