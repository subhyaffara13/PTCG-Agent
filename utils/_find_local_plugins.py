
def _find_local_plugins(
    cfg: configparser.RawConfigParser,
) -> Generator[Plugin]:
    for plugin_type in ("extension", "report"):
        group = f"flake8.{plugin_type}"
        for plugin_s in utils.parse_comma_separated_list(
            cfg.get("flake8:local-plugins", plugin_type, fallback="").strip(),
            regexp=utils.LOCAL_PLUGIN_LIST_RE,
        ):
            name, _, entry_str = plugin_s.partition("=")
            name, entry_str = name.strip(), entry_str.strip()
            ep = importlib.metadata.EntryPoint(name, entry_str, group)
            yield Plugin("local", "local", ep)

