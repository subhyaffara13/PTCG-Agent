
def _pretty_print_redis_config(redis_kwargs: dict) -> None:
    """Pretty print the Redis configuration using rich with sensitive data masking"""
    try:
        import logging

        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text

        if not verbose_logger.isEnabledFor(logging.DEBUG):
            return

        console = Console()

        # Initialize the sensitive data masker
        masker = SensitiveDataMasker()

        # Mask sensitive data in redis_kwargs
        masked_redis_kwargs = masker.mask_dict(redis_kwargs)

        # Create main panel title
        title = Text("Redis Configuration", style="bold blue")

        # Create configuration table
        config_table = Table(
            title="🔧 Redis Connection Parameters",
            show_header=True,
            header_style="bold magenta",
            title_justify="left",
        )
        config_table.add_column("Parameter", style="cyan", no_wrap=True)
        config_table.add_column("Value", style="yellow")

        # Add rows for each configuration parameter
        for key, value in masked_redis_kwargs.items():
            if value is not None:
                # Special handling for complex objects
                if isinstance(value, list):
                    if key == "startup_nodes" and value:
                        # Special handling for cluster nodes
                        value_str = f"[{len(value)} cluster nodes]"
                    elif key == "sentinel_nodes" and value:
                        # Special handling for sentinel nodes
                        value_str = f"[{len(value)} sentinel nodes]"
                    else:
                        value_str = str(value)
                else:
                    value_str = str(value)

                config_table.add_row(key, value_str)

        # Determine connection type
        connection_type = "Standard Redis"
        if masked_redis_kwargs.get("startup_nodes"):
            connection_type = "Redis Cluster"
        elif masked_redis_kwargs.get("sentinel_nodes"):
            connection_type = "Redis Sentinel"
        elif masked_redis_kwargs.get("url"):
            connection_type = "Redis (URL-based)"

        # Create connection type info
        info_table = Table(
            title="📊 Connection Info",
            show_header=True,
            header_style="bold green",
            title_justify="left",
        )
        info_table.add_column("Property", style="cyan", no_wrap=True)
        info_table.add_column("Value", style="yellow")
        info_table.add_row("Connection Type", connection_type)

        # Print everything in a nice panel
        console.print("\n")
        console.print(Panel(title, border_style="blue"))
        console.print(info_table)
        console.print(config_table)
        console.print("\n")

    except ImportError:
        # Fallback to simple logging if rich is not available
        masker = SensitiveDataMasker()
        masked_redis_kwargs = masker.mask_dict(redis_kwargs)
        verbose_logger.info(f"Redis configuration: {masked_redis_kwargs}")
    except Exception as e:
        verbose_logger.error(f"Error pretty printing Redis configuration: {e}")

