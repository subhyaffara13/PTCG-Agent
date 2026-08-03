import subprocess
import sys

def test_no_timezone_data():
    # https://github.com/pandas-dev/pandas/pull/63335
    # Test error message when timezone data is not available.
    msg = "'No time zone found with key Europe/Brussels'"
    code = textwrap.dedent(
        f"""\
        import sys, zoneinfo, pandas as pd
        sys.modules['tzdata'] = None
        zoneinfo.reset_tzpath(['/path/to/nowhere'])
        try:
            pd.to_datetime('2012-01-01').tz_localize('Europe/Brussels')
        except zoneinfo.ZoneInfoNotFoundError as err:
            assert str(err) == "{msg}"
        """
    )
    subprocess.check_call([sys.executable, "-c", code])

