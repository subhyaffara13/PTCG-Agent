import time

def test_chrono_different_resolutions():
    resolutions = m.different_resolutions()
    time = datetime.datetime.now()
    resolutions.timestamp_h = time
    resolutions.timestamp_m = time
    resolutions.timestamp_s = time
    resolutions.timestamp_ms = time
    resolutions.timestamp_us = time

