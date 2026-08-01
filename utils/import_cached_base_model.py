
def import_cached_base_model() -> type['BaseModel']:
    from pydantic import BaseModel

    return BaseModel

