import os
import re

def munge_exc(e, *, suppress_suffix=True, suppress_prefix=True, file=None, skip=0):
    from torch._dynamo.trace_rules import _as_posix_path

    if file is None:
        file = inspect.stack()[1 + skip].filename  # skip one frame

    file = _as_posix_path(file)
    s = _as_posix_path(str(e))

    # Remove everything that looks like stack frames in NOT this file
    def repl_frame(m):
        if m.group(2) != file:
            return ""
        # Don't accept top-level, even for this script, these will wobble
        # depending on how the testing script was invoked
        if m.group(3) == "<module>":
            return ""

        return m.group(0)

    s = re.sub(
        r'( *)File "([^"]+)", line \d+, in (.+)\n(\1  .+\n( +[~^]+ *\n)?)+',
        repl_frame,
        s,
    )
    s = re.sub(r"line \d+", "line N", s)
    s = re.sub(r".py:\d+", ".py:N", s)
    s = re.sub(r'https:/([a-zA-Z0-9_.-]+)', r'https://\1', s)
    s = re.sub(file, _as_posix_path(os.path.basename(file)), s)
    s = re.sub(_as_posix_path(os.path.join(os.path.dirname(torch.__file__), "")), "", s)
    # 3.10 CALL_FUNCTION bytecode compatibility for dynamo graph break messages
    s = re.sub(
        r"attempting to trace CALL_FUNCTION:.*$",
        "attempting to trace CALL: a function call, e.g. f(x, y):",
        s,
        flags=re.MULTILINE,
    )
    if suppress_suffix:
        s = re.sub(r"\n*Set TORCH_LOGS.+", "", s, flags=re.DOTALL)
        s = re.sub(r"\n*You can suppress this exception.+", "", s, flags=re.DOTALL)
        s = re.sub(r"\n*Set TORCHDYNAMO_VERBOSE=1.+", "", s, flags=re.DOTALL)
    if suppress_prefix:
        s = re.sub(r"Cannot export model.+\n\n", "", s)
    s = re.sub(r" +$", "", s, flags=re.MULTILINE)
    return s

