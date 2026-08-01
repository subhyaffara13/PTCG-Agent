
def test_parse_datetime_string_with_reso_dayfirst(dayfirst, input):
    with option_context("display.date_dayfirst", dayfirst):
        except_out_dateutil, result = _helper_hypothesis_delimited_date(
            parsing.parse_datetime_string_with_reso, input
        )

        except_in_dateutil, expected = _helper_hypothesis_delimited_date(
            du_parse,
            input,
            default=datetime(1, 1, 1),
            dayfirst=dayfirst,
            yearfirst=False,
        )
        assert except_out_dateutil == except_in_dateutil
        assert result[0] == expected

