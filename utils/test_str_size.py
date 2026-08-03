import subprocess
import sys

def test_str_size():
    # GH#21758
    a = "a"
    expected = sys.getsizeof(a)
    pyexe = sys.executable.replace("\\", "/")
    call = [
        pyexe,
        "-c",
        "a='a';import sys;sys.getsizeof(a);import pandas;print(sys.getsizeof(a));",
    ]
    result = subprocess.check_output(call).decode()[-4:-1].strip("\n")
    assert int(result) == int(expected)

