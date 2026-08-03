import logging
import re

def test_logging(should_trace):
    buffer = StringIO()
    handler = logging.StreamHandler(buffer)
    logger.addHandler(handler)
    try:
        dill.dumps(test_obj)
        if should_trace:
            regex = re.compile(r'(\S*┬ \w.*[^)]'              # begin pickling object
                               r'|│*└ # \w.* \[\d+ (\wi)?B])' # object written (with size)
                               )
            for line in buffer.getvalue().splitlines():
                assert regex.fullmatch(line)
            return buffer.getvalue()
        else:
            assert buffer.getvalue() == ""
    finally:
        logger.removeHandler(handler)
        buffer.close()

