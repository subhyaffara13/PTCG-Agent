
def exception_handler(
    e: Exception,
    code: CodeType,
    frame: DynamoFrameType | None = None,
    export: bool = False,
) -> None:
    record_filename = None
    if hasattr(e, "exec_record"):
        record_filename = gen_record_file_name(e, code)
        write_record_to_file(record_filename, e.exec_record)
        e.record_filename = record_filename  # type: ignore[attr-defined]

    augment_exc_message(e, export=export)

