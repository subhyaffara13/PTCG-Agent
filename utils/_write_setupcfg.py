
def _write_setupcfg(root, options):
    if not options:
        print("~~~~~ **NO** setup.cfg ~~~~~")
        return
    setupcfg = ConfigParser()
    setupcfg.add_section("options")
    for key, value in options.items():
        if key == "packages.find":
            setupcfg.add_section(f"options.{key}")
            setupcfg[f"options.{key}"].update(value)
        elif isinstance(value, list):
            setupcfg["options"][key] = ", ".join(value)
        elif isinstance(value, dict):
            str_value = "\n".join(f"\t{k} = {v}" for k, v in value.items())
            setupcfg["options"][key] = "\n" + str_value
        else:
            setupcfg["options"][key] = str(value)
    with open(root / "setup.cfg", "w", encoding="utf-8") as f:
        setupcfg.write(f)
    print("~~~~~ setup.cfg ~~~~~")
    print((root / "setup.cfg").read_text(encoding="utf-8"))

