
def field_singleton_sub_fields_schema(
    field: ModelField,
    *,
    by_alias: bool,
    model_name_map: Dict[TypeModelOrEnum, str],
    ref_template: str,
    schema_overrides: bool = False,
    ref_prefix: Optional[str] = None,
    known_models: TypeModelSet,
) -> Tuple[Dict[str, Any], Dict[str, Any], Set[str]]:
    """
    This function is indirectly used by ``field_schema()``, you probably should be using that function.

    Take a list of Pydantic ``ModelField`` from the declaration of a type with parameters, and generate their
    schema. I.e., fields used as "type parameters", like ``str`` and ``int`` in ``Tuple[str, int]``.
    """
    sub_fields = cast(List[ModelField], field.sub_fields)
    definitions = {}
    nested_models: Set[str] = set()
    if len(sub_fields) == 1:
        return field_type_schema(
            sub_fields[0],
            by_alias=by_alias,
            model_name_map=model_name_map,
            schema_overrides=schema_overrides,
            ref_prefix=ref_prefix,
            ref_template=ref_template,
            known_models=known_models,
        )
    else:
        s: Dict[str, Any] = {}
        # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#discriminator-object
        field_has_discriminator: bool = field.discriminator_key is not None
        if field_has_discriminator:
            assert field.sub_fields_mapping is not None

            discriminator_models_refs: Dict[str, Union[str, Dict[str, Any]]] = {}

            for discriminator_value, sub_field in field.sub_fields_mapping.items():
                if isinstance(discriminator_value, Enum):
                    discriminator_value = str(discriminator_value.value)
                # sub_field is either a `BaseModel` or directly an `Annotated` `Union` of many
                if is_union(get_origin(sub_field.type_)):
                    sub_models = get_sub_types(sub_field.type_)
                    discriminator_models_refs[discriminator_value] = {
                        model_name_map[sub_model]: get_schema_ref(
                            model_name_map[sub_model], ref_prefix, ref_template, False
                        )
                        for sub_model in sub_models
                    }
                else:
                    sub_field_type = sub_field.type_
                    if hasattr(sub_field_type, '__pydantic_model__'):
                        sub_field_type = sub_field_type.__pydantic_model__

                    discriminator_model_name = model_name_map[sub_field_type]
                    discriminator_model_ref = get_schema_ref(discriminator_model_name, ref_prefix, ref_template, False)
                    discriminator_models_refs[discriminator_value] = discriminator_model_ref['$ref']

            s['discriminator'] = {
                'propertyName': field.discriminator_alias if by_alias else field.discriminator_key,
                'mapping': discriminator_models_refs,
            }

        sub_field_schemas = []
        for sf in sub_fields:
            sub_schema, sub_definitions, sub_nested_models = field_type_schema(
                sf,
                by_alias=by_alias,
                model_name_map=model_name_map,
                schema_overrides=schema_overrides,
                ref_prefix=ref_prefix,
                ref_template=ref_template,
                known_models=known_models,
            )
            definitions.update(sub_definitions)
            if schema_overrides and 'allOf' in sub_schema:
                # if the sub_field is a referenced schema we only need the referenced
                # object. Otherwise we will end up with several allOf inside anyOf/oneOf.
                # See https://github.com/pydantic/pydantic/issues/1209
                sub_schema = sub_schema['allOf'][0]

            if sub_schema.keys() == {'discriminator', 'oneOf'}:
                # we don't want discriminator information inside oneOf choices, this is dealt with elsewhere
                sub_schema.pop('discriminator')
            sub_field_schemas.append(sub_schema)
            nested_models.update(sub_nested_models)
        s['oneOf' if field_has_discriminator else 'anyOf'] = sub_field_schemas
        return s, definitions, nested_models

