# -*- coding: utf-8 -*-

from .defaults import SECTION_SEPARATOR


class Field(object):
    def __init__(self, value, description=None, index=None, message=None):
        self._description = description
        self._index = index
        self._message = message

        self._raw_value = value
        self._value = self.parse(value)

    def parse(self, value):
        return value

    def __len__(self):
        return len(self._raw_value)

    def __bytes__(self):
        return self.value

    def __str__(self):
        return self.value.decode("utf-8")

    @property
    def value(self):
        return self._value

    @property
    def description(self):
        return self._description

    @property
    def index(self):
        return self._index


class CompositeFieldMixin(object):
    """
    Composite field mixin.
    """

    def parse(self, value):
        section_separator = (self._message.section_separator
                                if self._message else SECTION_SEPARATOR)

        parsed_value = []
        for _def, _data in zip(self._definition, value.split(section_separator)):
            i, cls_name, cls_desc = _def
            cls = resolve_field(cls_name)
            parsed_value.append((i, cls(_data, cls_desc, i, self._message)))

        return parsed_value

    @property
    def value(self):
        return b" ".join(bytes(x[1]) for x in self._value)


class STField(Field):
    """
    String representation on hl7 protocol.
    """
    pass


class IDField(Field):
    pass


class ISField(Field):
    pass


class CEField(Field):
    pass


class SIField(Field):
    pass


class CXField(CompositeFieldMixin, Field):
    """
    Extended composite id with check digit.
    """

    _definition = [
        (0, "ST", "ID"),
        (1, "ST", "Check digit"),
        (2, "ID", "Check digit"),
        (3, "HD", "Assigning authority"),
        (4, "IS", "Identifier type code"),
        (5, "HD", "Assigning facility"),
    ]


class XPNField(Field):
    """
    Extended person name representation.
    """

    def parse(self, value):
        value = value.replace(b"&", SECTION_SEPARATOR)
        return value.split(SECTION_SEPARATOR)

    @property
    def value(self):
        return b" ".join(self._value)


class TSField(Field):
    """
    Timestamp representation on hl7 protocol.
    """
    pass


class XADField(CompositeFieldMixin, Field):
    _definition = [
        (0, "ST", "Street address"),
        (1, "ST", "Other destination"),
        (2, "ST", "City"),
        (3, "ST", "State or Province"),
        (4, "ST", "Zip or postal code"),
        (5, "ID", "Country"),
        (6, "ID", "Address type"),
        (7, "ST", "Other geographical designation"),
        (8, "IS", "country/parish code"),
        (9, "IS", "census tract"),
        (10, "ID", "address representation code"),
        # TODO: finalize this
    ]


class HDField(Field):
    pass


class CMField(Field):
    pass


class PTField(Field):
    pass


fields_dict = {
    'XAD': XADField,
    'TS': TSField,
    'XPN': XPNField,
    'ST': STField,
    'ID': IDField,
    'IS': ISField,
    'CE': CEField,
    'SI': SIField,
    'CX': CXField,
    'HD': HDField,
    'CM': CMField,
    'PT': PTField,
}


def resolve_field(fieldname):
    global fields_dict

    if fieldname in fields_dict:
        return fields_dict[fieldname]
    raise ValueError("{0} does not exist".format(fieldname))
