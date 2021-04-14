from django.core.exceptions import ValidationError


def cannot_starts_with_lower_validator(string: str):
    if string[0].islower():
        raise ValidationError('Cannot starts with lower case')
    return string


def cannot_contain_digits_validator(string: str):
    if any(char.isdigit() for char in string):
        raise ValidationError('Cannot contain digits', 'invalid')
    return string


def cannot_contain_punctuation_validator(string: str):
    from string import punctuation as p
    if any(char in p for char in string):
        raise ValidationError('Cannot contain punctuation signs', 'invalid')
    return string
