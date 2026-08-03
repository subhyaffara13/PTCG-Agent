from typing import Optional

def _xs_string_mod_apply(v: str, t: Optional[XmlStringSerializationType]) -> str:
    mod = __XS_STRING_MODS.get(t)  # type: ignore[arg-type]
    return mod(v) if mod else v

