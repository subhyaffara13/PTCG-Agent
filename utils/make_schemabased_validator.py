from typing import Union

def make_schemabased_validator(output_format: Literal[OutputFormat.JSON], schema_version: 'SchemaVersion'
                               ) -> 'JsonValidator':
    ...  # pragma: no cover


def make_schemabased_validator(output_format: Literal[OutputFormat.XML], schema_version: 'SchemaVersion'
                               ) -> 'XmlValidator':
    ...  # pragma: no cover


def make_schemabased_validator(output_format: OutputFormat, schema_version: 'SchemaVersion'
                               ) -> Union['JsonValidator', 'XmlValidator']:
    ...  # pragma: no cover


def make_schemabased_validator(output_format: OutputFormat, schema_version: 'SchemaVersion'
                               ) -> 'BaseSchemabasedValidator':
    """Get the default Schema-based Validator for a certain :class:`OutputFormat`.

    Raises error when no instance could be made.
    """
    if TYPE_CHECKING:  # pragma: no cover
        Validator: type[BaseSchemabasedValidator]  # noqa:N806
    if OutputFormat.JSON is output_format:
        from .json import JsonValidator as Validator
    elif OutputFormat.XML is output_format:
        from .xml import XmlValidator as Validator
    else:
        raise ValueError(f'Unexpected output_format: {output_format!r}')
    return Validator(schema_version)

