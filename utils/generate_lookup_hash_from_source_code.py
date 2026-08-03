import re

def generate_lookup_hash_from_source_code(size_hints_str: str, source_code: str) -> str:
    # Name agnostic + strip white space
    fn_strip_name = re.sub(triton_name_sub, "(", source_code.strip(), count=1)
    hash_str = size_hints_str + fn_strip_name
    fn_hash = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

    return fn_hash

