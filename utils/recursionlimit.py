import sys

def recursionlimit(n):
    o = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(n)
        yield
    finally:
        sys.setrecursionlimit(o)

