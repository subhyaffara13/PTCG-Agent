
def make_site_dir(target):
    """
    Add a sitecustomize.py module in target to cause
    target to be added to site dirs such that .pth files
    are processed there.
    """
    sc = target / 'sitecustomize.py'
    target_str = str(target)
    tmpl = '__import__("site").addsitedir({target_str!r})'
    sc.write_text(tmpl.format(**locals()), encoding='utf-8')

