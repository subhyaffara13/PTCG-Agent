import re
import math


def test_mathtext_exceptions(math, msg):
    parser = mathtext.MathTextParser('agg')
    match = re.escape(msg) if isinstance(msg, str) else msg
    with pytest.raises(ValueError, match=match):
        parser.parse(math)

