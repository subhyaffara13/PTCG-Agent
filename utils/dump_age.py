
def dump_age(age: timedelta | int | None = None) -> str | None:
    """Formats the duration as a base-10 integer.

    :param age: should be an integer number of seconds,
                a :class:`datetime.timedelta` object, or,
                if the age is unknown, `None` (default).
    """
    if age is None:
        return None
    if isinstance(age, timedelta):
        age = int(age.total_seconds())
    else:
        age = int(age)

    if age < 0:
        raise ValueError("age cannot be negative")

    return str(age)

