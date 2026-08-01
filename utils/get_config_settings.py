
def get_config_settings():
    """Get configuration settings."""
    config = {}
    for plugin in extension_loader.MANAGER.plugins:
        fn_name = plugin.name
        function = plugin.plugin

        # if a function takes config...
        if hasattr(function, "_takes_config"):
            fn_module = importlib.import_module(function.__module__)

            # call the config generator if it exists
            if hasattr(fn_module, "gen_config"):
                config[fn_name] = fn_module.gen_config(function._takes_config)

    return yaml.safe_dump(config, default_flow_style=False)

