
def _classify_key_size(config, key_type, key_size):
    if isinstance(key_size, str):
        # size provided via a variable - can't process it at the moment
        return

    key_sizes = {
        "DSA": [
            (config["weak_key_size_dsa_high"], bandit.HIGH),
            (config["weak_key_size_dsa_medium"], bandit.MEDIUM),
        ],
        "RSA": [
            (config["weak_key_size_rsa_high"], bandit.HIGH),
            (config["weak_key_size_rsa_medium"], bandit.MEDIUM),
        ],
        "EC": [
            (config["weak_key_size_ec_high"], bandit.HIGH),
            (config["weak_key_size_ec_medium"], bandit.MEDIUM),
        ],
    }

    for size, level in key_sizes[key_type]:
        if key_size < size:
            return bandit.Issue(
                severity=level,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.INADEQUATE_ENCRYPTION_STRENGTH,
                text="%s key sizes below %d bits are considered breakable. "
                % (key_type, size),
            )

