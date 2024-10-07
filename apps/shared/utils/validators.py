from prompt_toolkit.validation import ValidationError


def validate_only_digits(value):
    value = value.replace('+','')
    if not value.isdigit():
        raise ValidationError("This field must only contain digits.")
