import json

import jsonschema
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import gettext as t


class JsonSchemaFormField(CharField):
    def __init__(self, *args, schema, **kwargs):
        self.schema = schema
        super().__init__(*args, **kwargs)

    def clean(self, value):
        try:
            instance = json.loads(value)
            jsonschema.validate(instance, self.schema)
        except json.JSONDecodeError as e:
            # Message written to match `IntegerField`, which uses the
            # imperative: "Enter a whole number."
            raise ValidationError(t('Enter valid JSON.') + ' ' + str(e))
        except jsonschema.exceptions.ValidationError as e:
            # `str(e)` is too verbose (it includes the entire schema)
            raise ValidationError(t('Enter valid JSON.') + ' ' + e.message)
        return value


class FreeTierThresholdField(JsonSchemaFormField):
    """
    Validates that the input has required properties with expected types
    """
    def __init__(self, *args, **kwargs):
        schema = {
            'type': 'object',
            'uniqueItems': True,
            'properties': {
                'storage': {'type': 'integer'},
                'data': {'type': 'integer'},
                'transcription_minutes': {'type': 'integer'},
                'translation_chars': {'type': 'integer'},
            },
            'required': [
                'storage',
                'data',
                'transcription_minutes',
                'translation_chars',
            ],
            'additionalProperties': False,
        }
        super().__init__(*args, schema=schema, **kwargs)


class MetadataFieldsListField(JsonSchemaFormField):
    """
    Validates that the input is an array of objects with "name" and "required"
    properties, e.g.
        [
            {"name": "important_field", "required": true},
            {"name": "whatever_field", "required": false},
            …
        ]
    """
    def __init__(self, *args, **kwargs):
        schema = {
            'type': 'array',
            'uniqueItems': True,
            'items': {
                'type': 'object',
                'required': ['name', 'required'],
                'additionalProperties': False,
                'properties': {
                    'name': {'type': 'string'},
                    'required': {'type': 'boolean'},
                },
            },
        }
        super().__init__(*args, schema=schema, **kwargs)


class MfaHelpTextField(JsonSchemaFormField):
    """
    Validates that the input is an object which contains at least the 'default'
    key.
    """
    def __init__(self, *args, **kwargs):
        schema = {
            'type': 'object',
            'uniqueItems': True,
            'properties': {
                'default': {'type': 'string'},
            },
            'required': ['default'],
            'additionalProperties': True,
        }
        super().__init__(*args, schema=schema, **kwargs)
