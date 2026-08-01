
def have_git() -> bool:
    """Can we run the git executable?"""
    try:
        subprocess.check_output(["git", "--help"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def have_git() -> bool:  # pragma: no cover
    """Can we run the git executable?"""
    try:
        subprocess.check_output(['git', '--help'])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False

