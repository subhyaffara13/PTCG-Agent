
def this_component() -> 'Component':
    """Deprecated — Alias of :func:`cyclonedx.contrib.this.builders.this_component`.

    .. deprecated:: next
        This re-export location is deprecated.
        Use ``from cyclonedx.contrib.this.builders import this_component`` instead.
        The exported symbol itself is NOT deprecated — only this import path.
    """
    return _this_component()


def this_component() -> Component:
    """Representation of this very python library as a :class:`cyclonedx.model.component.Component`."""
    return Component(
        type=ComponentType.LIBRARY,
        group='CycloneDX',
        name='cyclonedx-python-lib',
        version=__ThisVersion or 'UNKNOWN',
        description='Python library for CycloneDX',
        licenses=(DisjunctiveLicense(id='Apache-2.0',
                                     acknowledgement=LicenseAcknowledgement.DECLARED),),
        external_references=(
            # let's assume this is not a fork
            ExternalReference(
                type=ExternalReferenceType.WEBSITE,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/#readme')
            ),
            ExternalReference(
                type=ExternalReferenceType.DOCUMENTATION,
                url=XsUri('https://cyclonedx-python-library.readthedocs.io/')
            ),
            ExternalReference(
                type=ExternalReferenceType.VCS,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib')
            ),
            ExternalReference(
                type=ExternalReferenceType.BUILD_SYSTEM,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/actions')
            ),
            ExternalReference(
                type=ExternalReferenceType.ISSUE_TRACKER,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/issues')
            ),
            ExternalReference(
                type=ExternalReferenceType.LICENSE,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE')
            ),
            ExternalReference(
                type=ExternalReferenceType.RELEASE_NOTES,
                url=XsUri('https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/CHANGELOG.md')
            ),
            # we cannot assert where the lib was fetched from, but we can give a hint
            ExternalReference(
                type=ExternalReferenceType.DISTRIBUTION,
                url=XsUri('https://pypi.org/project/cyclonedx-python-lib/')
            ),
        ),
        # to be extended...
    )

