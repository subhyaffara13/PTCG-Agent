
def test_formatters(Formatter, regex, direction, factor, values):
    fmt = Formatter()
    result = fmt(direction, factor, values)

    prev_degree = prev_minute = prev_second = None
    for tick, value in zip(result, values):
        m = regex.match(tick)
        assert m is not None, f'{tick!r} is not an expected tick format.'

        sign = sum(m.group(sign + '_sign') is not None
                   for sign in ('degree', 'minute', 'second'))
        assert sign <= 1, f'Only one element of tick {tick!r} may have a sign.'
        sign = 1 if sign == 0 else -1

        degree = float(m.group('degree') or prev_degree or 0)
        minute = float(m.group('minute') or prev_minute or 0)
        second = float(m.group('second') or prev_second or 0)
        if Formatter == FormatterHMS:
            # 360 degrees as plot range -> 24 hours as labelled range
            expected_value = pytest.approx((value // 15) / factor)
        else:
            expected_value = pytest.approx(value / factor)
        assert sign * dms2float(degree, minute, second) == expected_value, \
            f'{tick!r} does not match expected tick value.'

        prev_degree = degree
        prev_minute = minute
        prev_second = second

