
def test_parse_datetime_string_with_reso_yearfirst(yearfirst, input):
    with option_context("display.date_yearfirst", yearfirst):
        except_out_dateutil, result = _helper_hypothesis_delimited_date(
            parsing.parse_datetime_string_with_reso, input
        )
        except_in_dateutil, expected = _helper_hypothesis_delimited_date(
            du_parse,
            input,
            default=datetime(1, 1, 1),
            dayfirst=False,
            yearfirst=yearfirst,
        )
        assert except_out_dateutil == except_in_dateutil
        assert result[0] == expected

