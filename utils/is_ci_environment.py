import os

def is_ci_environment() -> bool:
    """
    Checking if running in a continuous integration environment by checking
    the PANDAS_CI environment variable.

    Returns
    -------
    bool
        True if the running in a continuous integration environment.
    """
    return os.environ.get("PANDAS_CI", "0") == "1"


def is_ci_environment():
    # Common CI variables
    ci_environment_variables = [
        'CI',        # Generic CI environment variable
        'CONTINUOUS_INTEGRATION',  # Generic CI environment variable
        'TRAVIS',    # Travis CI
        'CIRCLECI',  # CircleCI
        'JENKINS',   # Jenkins
        'GITLAB_CI',  # GitLab CI
        'GITHUB_ACTIONS',  # GitHub Actions
        'TEAMCITY_VERSION'  # TeamCity
        # Add other CI environment variables as needed
    ]

    for env_var in ci_environment_variables:
        if os.getenv(env_var):
            return True

    return False

