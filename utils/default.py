import os
from typing import Optional

def default(name: str) -> DefaultHandler:
    """A decorator which assigns a dynamic default for a Trait on a HasTraits object.

    Parameters
    ----------
    name
        The str name of the Trait on the object whose default should be generated.

    Notes
    -----
    Unlike observers and validators which are properties of the HasTraits
    instance, default value generators are class-level properties.

    Besides, default generators are only invoked if they are registered in
    subclasses of `this_type`.

    ::

        class A(HasTraits):
            bar = Int()

            @default('bar')
            def get_bar_default(self):
                return 11

        class B(A):
            bar = Float()  # This trait ignores the default generator defined in
                           # the base class A

        class C(B):

            @default('bar')
            def some_other_default(self):  # This default generator should not be
                return 3.0                 # ignored since it is defined in a
                                           # class derived from B.a.this_class.
    """
    if not isinstance(name, str):
        raise TypeError("Trait name must be a string or All, not %r" % name)
    return DefaultHandler(name)


def Default(value: DefaultType) -> DefaultType:
    """
    You shouldn't use this function directly.

    It's used internally to recognize when a default value has been overwritten, even
    if the new value is `None`.
    """
    return DefaultPlaceholder(value)  # type: ignore


def default(
    scopes: Optional[Sequence[str]] = None,
    request: Optional["google.auth.transport.Request"] = None,
    quota_project_id: Optional[str] = None,
    default_scopes: Optional[Sequence[str]] = None,
) -> tuple["google.auth.credentials.Credentials", Optional[str]]:
    """Gets the default credentials for the current environment.

    `Application Default Credentials`_ provides an easy way to obtain
    credentials to call Google APIs for server-to-server or local applications.
    This function acquires credentials from the environment in the following
    order:

    1. If the environment variable ``GOOGLE_APPLICATION_CREDENTIALS`` is set
       to the path of a valid service account JSON private key file, then it is
       loaded and returned. The project ID returned is the project ID defined
       in the service account file if available (some older files do not
       contain project ID information).

       If the environment variable is set to the path of a valid external
       account JSON configuration file (workload identity federation), then the
       configuration file is used to determine and retrieve the external
       credentials from the current environment (AWS, Azure, etc).
       These will then be exchanged for Google access tokens via the Google STS
       endpoint.
       The project ID returned in this case is the one corresponding to the
       underlying workload identity pool resource if determinable.

       If the environment variable is set to the path of a valid GDCH service
       account JSON file (`Google Distributed Cloud Hosted`_), then a GDCH
       credential will be returned. The project ID returned is the project
       specified in the JSON file.
    2. If the `Google Cloud SDK`_ is installed and has application default
       credentials set they are loaded and returned.

       To enable application default credentials with the Cloud SDK run::

            gcloud auth application-default login

       If the Cloud SDK has an active project, the project ID is returned. The
       active project can be set using::

            gcloud config set project

    3. If the application is running in the `App Engine standard environment`_
       (first generation) then the credentials and project ID from the
       `App Identity Service`_ are used.
    4. If the application is running in `Compute Engine`_ or `Cloud Run`_ or
       the `App Engine flexible environment`_ or the `App Engine standard
       environment`_ (second generation) then the credentials and project ID
       are obtained from the `Metadata Service`_.
    5. If no credentials are found,
       :class:`~google.auth.exceptions.DefaultCredentialsError` will be raised.

    .. _Application Default Credentials: https://developers.google.com\
            /identity/protocols/application-default-credentials
    .. _Google Cloud SDK: https://cloud.google.com/sdk
    .. _App Engine standard environment: https://cloud.google.com/appengine
    .. _App Identity Service: https://cloud.google.com/appengine/docs/python\
            /appidentity/
    .. _Compute Engine: https://cloud.google.com/compute
    .. _App Engine flexible environment: https://cloud.google.com\
            /appengine/flexible
    .. _Metadata Service: https://cloud.google.com/compute/docs\
            /storing-retrieving-metadata
    .. _Cloud Run: https://cloud.google.com/run
    .. _Google Distributed Cloud Hosted: https://cloud.google.com/blog/topics\
            /hybrid-cloud/announcing-google-distributed-cloud-edge-and-hosted

    Example::

        import google.auth

        credentials, project_id = google.auth.default()

    Args:
        scopes (Sequence[str]): The list of scopes for the credentials. If
            specified, the credentials will automatically be scoped if
            necessary.
        request (Optional[google.auth.transport.Request]): An object used to make
            HTTP requests. This is used to either detect whether the application
            is running on Compute Engine or to determine the associated project
            ID for a workload identity pool resource (external account
            credentials). If not specified, then it will either use the standard
            library http client to make requests for Compute Engine credentials
            or a google.auth.transport.requests.Request client for external
            account credentials.
        quota_project_id (Optional[str]): The project ID used for
            quota and billing.
        default_scopes (Optional[Sequence[str]]): Default scopes passed by a
            Google client library. Use 'scopes' for user-defined scopes.
    Returns:
        Tuple[~google.auth.credentials.Credentials, Optional[str]]:
            the current environment's credentials and project ID. Project ID
            may be None, which indicates that the Project ID could not be
            ascertained from the environment.

    Raises:
        ~google.auth.exceptions.DefaultCredentialsError:
            If no credentials were found, or if the credentials found were
            invalid.
    """
    from google.auth.credentials import with_scopes_if_required
    from google.auth.credentials import CredentialsWithQuotaProject

    explicit_project_id = os.environ.get(
        environment_vars.PROJECT, os.environ.get(environment_vars.LEGACY_PROJECT)
    )

    checkers = (
        # Avoid passing scopes here to prevent passing scopes to user credentials.
        # with_scopes_if_required() below will ensure scopes/default scopes are
        # safely set on the returned credentials since requires_scopes will
        # guard against setting scopes on user credentials.
        lambda: _get_explicit_environ_credentials(quota_project_id=quota_project_id),
        lambda: _get_gcloud_sdk_credentials(quota_project_id=quota_project_id),
        _get_gae_credentials,
        lambda: _get_gce_credentials(request, quota_project_id=quota_project_id),
    )

    for checker in checkers:
        credentials, project_id = checker()
        if credentials is not None:
            credentials = with_scopes_if_required(
                credentials, scopes, default_scopes=default_scopes
            )

            effective_project_id = explicit_project_id or project_id

            # For external account credentials, scopes are required to determine
            # the project ID. Try to get the project ID again if not yet
            # determined.
            if not effective_project_id and callable(
                getattr(credentials, "get_project_id", None)
            ):
                if request is None:
                    import google.auth.transport.requests

                    request = google.auth.transport.requests.Request()
                effective_project_id = credentials.get_project_id(request=request)

            if quota_project_id and isinstance(
                credentials, CredentialsWithQuotaProject
            ):
                credentials = credentials.with_quota_project(quota_project_id)

            if not effective_project_id:
                _LOGGER.warning(
                    "No project ID could be determined. Consider running "
                    "`gcloud config set project` or setting the %s "
                    "environment variable",
                    environment_vars.PROJECT,
                )
            return credentials, effective_project_id

    raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS)


def Default():
  return _DEFAULT


def Default():
  """Returns the default SymbolDatabase."""
  return _DEFAULT

