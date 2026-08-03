import json
import sys

def get_message(dimension_process):
    raw = dimension_process.stderr.readline()
    try:
        res = json.loads(raw)
        return res
    except Exception:
        print("Engine Exception")
        err_stack = dimension_process.stderr.readlines(100)
        # err_stack = [raw, *err_stack]
        # print(err_stack)
        for m in err_stack:
            if len(m) < 1000:
                print(m.decode(), file=sys.stderr)
            else:
                print("...", file=sys.stderr)

