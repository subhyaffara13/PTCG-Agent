import os

def get_env():
    env = os.getenv("KAGGLE_API_ENVIRONMENT")
    if env is None or env == "PROD":
        return KaggleEnv.PROD
    if env == "LOCALHOST":
        return KaggleEnv.LOCAL
    if env == "ADMIN":
        return KaggleEnv.ADMIN
    if env == "STAGING":
        return KaggleEnv.STAGING
    if env == "QA":
        return KaggleEnv.QA
    if env == "TEST":
        return KaggleEnv.TEST
    raise Exception(f'Unrecognized value in KAGGLE_API_ENVIRONMENT: "{env}"')

