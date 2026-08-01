
def get_writer(engine_name: str) -> ExcelWriter_t:
    try:
        return _writers[engine_name]
    except KeyError as err:
        raise ValueError(f"No Excel writer '{engine_name}'") from err

