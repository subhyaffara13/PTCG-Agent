from typing import Union

def make_outputter(bom: 'Bom', output_format: Literal[OutputFormat.JSON],
                   schema_version: SchemaVersion) -> 'JsonOutputter':
    ...  # pragma: no cover


def make_outputter(bom: 'Bom', output_format: Literal[OutputFormat.XML],
                   schema_version: SchemaVersion) -> 'XmlOutputter':
    ...  # pragma: no cover


def make_outputter(bom: 'Bom', output_format: OutputFormat,
                   schema_version: SchemaVersion) -> Union['XmlOutputter', 'JsonOutputter']:
    ...  # pragma: no cover


def make_outputter(bom: 'Bom', output_format: OutputFormat, schema_version: SchemaVersion) -> BaseOutput:
    """
    Helper method to quickly get the correct output class/formatter.

    Pass in your BOM and optionally an output format and schema version (defaults to XML and latest schema version).


    Raises error when no instance could be made.

    :param bom: Bom
    :param output_format: OutputFormat
    :param schema_version: SchemaVersion
    :return: BaseOutput
    """
    if TYPE_CHECKING:  # pragma: no cover
        BY_SCHEMA_VERSION: Mapping[SchemaVersion, type[BaseOutput]]  # noqa:N806
    if OutputFormat.JSON is output_format:
        from .json import BY_SCHEMA_VERSION
    elif OutputFormat.XML is output_format:
        from .xml import BY_SCHEMA_VERSION
    else:
        raise ValueError(f'Unexpected output_format: {output_format!r}')

    klass = BY_SCHEMA_VERSION.get(schema_version, None)
    if klass is None:
        raise ValueError(f'Unknown {output_format.name}/schema_version: {schema_version!r}')
    return klass(bom)

