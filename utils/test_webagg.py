import re
import sys
import time

def test_webagg():
    pytest.importorskip("tornado")
    source = (inspect.getsource(_test_interactive_impl) +
              "\n_test_interactive_impl()")
    rc = '{"backend": "webagg"}'
    with _WaitForStringPopen([sys.executable, "-c", source, rc]) as proc:
        try:
            buf = proc.wait_for('Press Ctrl+C')
            url = re.search(r'visit (https?:\/\/\S+)', buf).group(1)
            timeout = time.perf_counter() + _test_timeout
            while True:
                try:
                    retcode = proc.poll()
                    # check that the subprocess for the server is not dead
                    assert retcode is None
                    with urllib.request.urlopen(url):
                        # Do nothing; we've just confirmed that we can connect.
                        break
                except urllib.error.URLError:
                    if time.perf_counter() > timeout:
                        pytest.fail("Failed to connect to the webagg server.")
                    else:
                        continue
            proc.send_signal(signal.SIGINT)
            assert proc.wait(timeout=_test_timeout) == 0
        finally:
            if proc.poll() is None:
                proc.kill()

