
def build_generic_google_code_archive_purl(uri):
    # https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com
    # /android-notifier/android-notifier-desktop-0.5.1-1.i386.rpm
    _, remaining_uri = uri.split(
        "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/"
    )
    if remaining_uri:  # android-notifier/android-notifier-desktop-0.5.1-1.i386.rpm
        split_remaining_uri = remaining_uri.split("/")
        # android-notifier, android-notifier-desktop-0.5.1-1.i386.rpm
        if split_remaining_uri:
            name = split_remaining_uri[0]  # android-notifier
            return PackageURL(
                type="generic",
                namespace="code.google.com",
                name=name,
                qualifiers={"download_url": uri},
            )

