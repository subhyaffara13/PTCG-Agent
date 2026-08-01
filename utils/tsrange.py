
def tsrange(*args, **kwargs):
    """Shortcut for `tqdm.contrib.slack.tqdm(range(*args), **kwargs)`."""
    return tqdm_slack(range(*args), **kwargs)

