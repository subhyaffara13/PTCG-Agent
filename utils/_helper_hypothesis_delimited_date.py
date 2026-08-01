
def _helper_hypothesis_delimited_date(call, date_string, **kwargs):
    msg, result = None, None
    try:
        result = call(date_string, **kwargs)
    except ValueError as err:
        msg = str(err)
    return msg, result

