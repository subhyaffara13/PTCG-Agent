
def print_dist_installation_info(latest: str, dist: BaseDistribution | None) -> None:
    if dist is not None:
        with indent_log():
            if dist.version == latest:
                write_output("INSTALLED: %s (latest)", dist.version)
            else:
                write_output("INSTALLED: %s", dist.version)
                if parse_version(latest).pre:
                    write_output(
                        "LATEST:    %s (pre-release; install"
                        " with `pip install --pre`)",
                        latest,
                    )
                else:
                    write_output("LATEST:    %s", latest)

