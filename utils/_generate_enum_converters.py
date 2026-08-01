
def _generate_enum_converters() -> str:
    """Generate C++ converter functions from serialized enum values to c10 enums."""

    def validate_mapping(
        enum_class: type[IntEnum],
        mapping: dict[int, str],
        enum_name: str,
        skip_values: set[int],
    ) -> None:
        """Validate that all enum values have corresponding c10 mappings."""
        for member in enum_class:
            if member.value in skip_values:
                continue
            if member.value not in mapping:
                raise SchemaUpdateError(
                    f"{enum_name}.{member.name} (value={member.value}) is missing "
                    f"from {enum_name.upper()}_TO_C10 mapping in schema.py. "
                    f"Please add the mapping to the c10 enum name."
                )

    # Validate that all enum values have mappings (except UNKNOWN values)
    validate_mapping(
        schema.ScalarType,
        schema.SCALAR_TYPE_TO_C10,
        "ScalarType",
        {schema.ScalarType.UNKNOWN},
    )
    validate_mapping(
        schema.Layout,
        schema.LAYOUT_TO_C10,
        "Layout",
        {schema.Layout.Unknown},
    )
    validate_mapping(
        schema.MemoryFormat,
        schema.MEMORY_FORMAT_TO_C10,
        "MemoryFormat",
        {schema.MemoryFormat.Unknown},
    )

    def generate_converter(
        name: str,
        c10_type: str,
        mapping: dict[int, str],
        max_value: int,
    ) -> str:
        lines: list[str] = []
        for i in range(max_value + 1):
            if i in mapping:
                lines.append(
                    f"      static_cast<int>(c10::{c10_type}::{mapping[i]}), // {i}"
                )
            else:
                lines.append(f"      kInvalid, // {i}")

        return f"""
inline c10::{c10_type} convertSerialized{name}(int serialized_value) {{
  constexpr int kInvalid = -1;
  constexpr int k{name}Map[] = {{
{chr(10).join(lines)}
  }};
  constexpr int kMapSize = sizeof(k{name}Map) / sizeof(k{name}Map[0]);

  TORCH_CHECK(
      serialized_value >= 0 && serialized_value < kMapSize,
      "Serialized {name} value out of range: ",
      serialized_value);
  int result = k{name}Map[serialized_value];
  TORCH_CHECK(
      result != kInvalid,
      "Invalid serialized {name} value: ",
      serialized_value);
  return static_cast<c10::{c10_type}>(result);
}}
"""

    scalar_type_converter = generate_converter(
        "ScalarType",
        "ScalarType",
        schema.SCALAR_TYPE_TO_C10,
        max(schema.SCALAR_TYPE_TO_C10.keys()),
    )
    layout_converter = generate_converter(
        "Layout",
        "Layout",
        schema.LAYOUT_TO_C10,
        max(schema.LAYOUT_TO_C10.keys()),
    )
    memory_format_converter = generate_converter(
        "MemoryFormat",
        "MemoryFormat",
        schema.MEMORY_FORMAT_TO_C10,
        max(schema.MEMORY_FORMAT_TO_C10.keys()),
    )

    return f"""
#pragma once

#include <c10/core/Layout.h>
#include <c10/core/MemoryFormat.h>
#include <c10/core/ScalarType.h>
#include <c10/util/Exception.h>

// Converter functions from serialized enum values (torch._export.serde.schema)
// to c10 enums. The serialized format has different enum values than c10.

namespace torch::aot_inductor {{
{scalar_type_converter}
{layout_converter}
{memory_format_converter}
}} // namespace torch::aot_inductor
"""

