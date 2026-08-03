import os

def has_local_docs():
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    main_page = os.path.join(pkg_dir, "generated", "index.html")
    return os.path.exists(main_page)

