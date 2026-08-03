from typing import Any

def set_discriminator_in_metadata(schema: CoreSchema, discriminator: Any) -> None:
    metadata = cast('CoreMetadata', schema.setdefault('metadata', {}))
    metadata['pydantic_internal_union_discriminator'] = discriminator

