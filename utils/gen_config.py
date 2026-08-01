
def gen_config(name):
    if name == "assert_used":
        return {"skips": []}


def gen_config(name):
    if name == "hardcoded_tmp_directory":
        return {"tmp_dirs": ["/tmp", "/var/tmp", "/dev/shm"]}  # nosec: B108


def gen_config(name):
    if name == "shell_injection":
        return {
            # Start a process using the subprocess module, or one of its
            # wrappers.
            "subprocess": [
                "subprocess.Popen",
                "subprocess.call",
                "subprocess.check_call",
                "subprocess.check_output",
                "subprocess.run",
            ],
            # Start a process with a function vulnerable to shell injection.
            "shell": [
                "os.system",
                "os.popen",
                "os.popen2",
                "os.popen3",
                "os.popen4",
                "popen2.popen2",
                "popen2.popen3",
                "popen2.popen4",
                "popen2.Popen3",
                "popen2.Popen4",
                "commands.getoutput",
                "commands.getstatusoutput",
                "subprocess.getoutput",
                "subprocess.getstatusoutput",
            ],
            # Start a process with a function that is not vulnerable to shell
            # injection.
            "no_shell": [
                "os.execl",
                "os.execle",
                "os.execlp",
                "os.execlpe",
                "os.execv",
                "os.execve",
                "os.execvp",
                "os.execvpe",
                "os.spawnl",
                "os.spawnle",
                "os.spawnlp",
                "os.spawnlpe",
                "os.spawnv",
                "os.spawnve",
                "os.spawnvp",
                "os.spawnvpe",
                "os.startfile",
            ],
        }


def gen_config(name):
    if name == "ssl_with_bad_version":
        return {
            "bad_protocol_versions": [
                "PROTOCOL_SSLv2",
                "SSLv2_METHOD",
                "SSLv23_METHOD",
                "PROTOCOL_SSLv3",  # strict option
                "PROTOCOL_TLSv1",  # strict option
                "SSLv3_METHOD",  # strict option
                "TLSv1_METHOD",
                "PROTOCOL_TLSv1_1",
                "TLSv1_1_METHOD",
            ]
        }  # strict option


def gen_config(name):
    if name == "markupsafe_xss":
        return {
            "extend_markup_names": [],
            "allowed_calls": [],
        }


def gen_config(name):
    if name == "try_except_continue":
        return {"check_typed_exception": False}


def gen_config(name):
    if name == "try_except_pass":
        return {"check_typed_exception": False}


def gen_config(name):
    if name == "weak_cryptographic_key":
        return {
            "weak_key_size_dsa_high": 1024,
            "weak_key_size_dsa_medium": 2048,
            "weak_key_size_rsa_high": 1024,
            "weak_key_size_rsa_medium": 2048,
            "weak_key_size_ec_high": 160,
            "weak_key_size_ec_medium": 224,
        }

