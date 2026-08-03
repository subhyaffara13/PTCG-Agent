import re

def _comment_stripped_hash(code: str) -> str:
    code = re.sub(r"#.*$", "", code, count=0, flags=re.MULTILINE)
    return torch._inductor.codecache.code_hash(code)

