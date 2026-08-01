
def _create_read_items(fqn: str, md: STORAGE_TYPES, obj: Any) -> list[ReadItem]:
    if not isinstance(md, BytesStorageMetadata):
        try:
            local_chunks = _create_chunk_list(obj)
        except ValueError as ex:
            raise ValueError(
                f"Invalid checkpoint metadata for {fqn}, "
                + f"expected BytesStorageMetadata but found {type(md)}",
            ) from ex

        return create_read_items_for_chunk_list(fqn, md, local_chunks)
    else:
        return [
            _create_read_item_for_byteio(
                dest_index=MetadataIndex(fqn),
                dest_offset=0,
                storage_index=MetadataIndex(fqn),
                storage_offset=0,
                length=0,
            )
        ]

