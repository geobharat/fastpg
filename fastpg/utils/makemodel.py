from datetime import datetime
from typing import Optional, Type, Union
from pydantic import BaseModel, create_model


def convert_model(model_name, current_dict):
    model_fields = {}
    for field_name, data_field_type in current_dict.items():
        if data_field_type == "bigint":
            field_type = int
        elif data_field_type == "integer":
            field_type = int
        elif data_field_type == "boolean":
            field_type = bool
        elif data_field_type == "text":
            field_type = str
        elif data_field_type == "numeric":
            field_type = float
        elif data_field_type == "timestamp with time zone":
            field_type = str
        else:
            field_type = str
        model_fields[field_name] = (Optional[str], None)
    model_fields["limit"] = (Optional[int], 10)
    model_fields["offset"] = (Optional[int], 0)
    return create_model(model_name, **model_fields)


def convert_op(op):
    if op == "eq":
        return "="
    elif op == "ne":
        return "!="
    elif op == "gt":
        return ">"
    elif op == "lt":
        return "<"
    elif op == "gte":
        return ">="
    elif op == "lte":
        return "<="
