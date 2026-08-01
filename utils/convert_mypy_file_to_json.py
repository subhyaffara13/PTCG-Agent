
def convert_mypy_file_to_json(self: MypyFile, cfg: Config) -> Json:
    return {
        ".class": "MypyFile",
        "_fullname": self._fullname,
        "names": convert_symbol_table(self.names, cfg),
        "is_stub": self.is_stub,
        "path": self.path,
        "is_partial_stub_package": self.is_partial_stub_package,
        "future_import_flags": sorted(self.future_import_flags),
    }

