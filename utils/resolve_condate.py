
def resolve_condate(cls):  # type: ignore[no-untyped-def]
    if cls.ge is not None:
        assert cls.gt is None, 'Set `gt` or `ge`, but not both'
        min_value = cls.ge
    elif cls.gt is not None:
        min_value = cls.gt + datetime.timedelta(days=1)
    else:
        min_value = datetime.date.min
    if cls.le is not None:
        assert cls.lt is None, 'Set `lt` or `le`, but not both'
        max_value = cls.le
    elif cls.lt is not None:
        max_value = cls.lt - datetime.timedelta(days=1)
    else:
        max_value = datetime.date.max
    return st.dates(min_value, max_value)

