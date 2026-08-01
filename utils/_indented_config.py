
def _indented_config(config: Config, indent: str) -> Config:
    if not indent:
        return config

    return Config(
        config=config,
        line_length=max(config.line_length - len(indent), 0),
        wrap_length=max(config.wrap_length - len(indent), 0),
        lines_after_imports=1,
        import_headings=config.import_headings if config.indented_import_headings else {},
        import_footers=config.import_footers if config.indented_import_headings else {},
    )

