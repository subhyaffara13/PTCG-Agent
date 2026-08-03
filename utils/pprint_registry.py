import re

def pprint_registry(
    print_registry: dict[str, EnvSpec] = registry,
    *,
    num_cols: int = 3,
    exclude_namespaces: list[str] | None = None,
    disable_print: bool = False,
) -> str | None:
    """Pretty prints all environments in the :attr:`registry`.

    Note:
        All arguments are keyword only

    Args:
        print_registry: Environment registry to be printed. By default, :attr:`registry`
        num_cols: Number of columns to arrange environments in, for display.
        exclude_namespaces: A list of namespaces to be excluded from printing. Helpful if only ALE environments are wanted.
        disable_print: Whether to return a string of all the namespaces and environment IDs
            or to print the string to console.
    """
    # Defaultdict to store environment ids according to namespace.
    namespace_envs: dict[str, list[str]] = defaultdict(list)
    max_justify = float("-inf")

    # Find the namespace associated with each environment spec
    for env_spec in print_registry.values():
        ns = env_spec.namespace

        if ns is None and isinstance(env_spec.entry_point, str):
            # Use regex to obtain namespace from entrypoints.
            env_entry_point = re.sub(r":\w+", "", env_spec.entry_point)
            split_entry_point = env_entry_point.split(".")

            if len(split_entry_point) >= 3:
                # If namespace is of the format:
                #  - gymnasium.envs.mujoco.ant_v4:AntEnv
                #  - gymnasium.envs.mujoco:HumanoidEnv
                ns = split_entry_point[2]
            elif len(split_entry_point) > 1:
                # If namespace is of the format - shimmy.atari_env
                ns = split_entry_point[1]
            else:
                # If namespace cannot be found, default to env name
                ns = env_spec.name

        namespace_envs[ns].append(env_spec.id)
        max_justify = max(max_justify, len(env_spec.name))

    # Iterate through each namespace and print environment alphabetically
    output: list[str] = []
    for ns, env_ids in namespace_envs.items():
        # Ignore namespaces to exclude.
        if exclude_namespaces is not None and ns in exclude_namespaces:
            continue

        # Print the namespace
        namespace_output = f"{'=' * 5} {ns} {'=' * 5}\n"

        # Reference: https://stackoverflow.com/a/33464001
        for count, env_id in enumerate(sorted(env_ids), 1):
            # Print column with justification.
            namespace_output += env_id.ljust(max_justify) + " "

            # Once all rows printed, switch to new column.
            if count % num_cols == 0:
                namespace_output = namespace_output.rstrip(" ")

                if count != len(env_ids):
                    namespace_output += "\n"

        output.append(namespace_output.rstrip(" "))

    if disable_print:
        return "\n".join(output)
    else:
        print("\n".join(output))

