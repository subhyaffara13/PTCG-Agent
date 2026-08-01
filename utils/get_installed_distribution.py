
def get_installed_distribution(name: str) -> BaseDistribution | None:
    env = get_default_environment()
    return env.get_distribution(name)

