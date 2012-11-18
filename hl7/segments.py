# -*- coding: utf-8 -*-

from .defaults import SEGMENT_SEPARATOR, SECTION_SEPARATOR, FIELD_SEPARATOR
from . import fields


class Segment(object):
    _fields = None
    _identifier = None
    _definition = None

    def __init__(self, data, message):
        self._message = message
        self._data = data.split(FIELD_SEPARATOR)
        self._fields = self.parse(self._data)

    def parse(self, data):
        parsed_data = []
        for _def, _data in zip(self._definition, self._data[1:]):
            i, size, cls_name, opt, desc = _def
            cls = fields.resolve_field(cls_name)
            #if len(_data) > size:
            #    import pdb; pdb.set_trace()
            #    raise RuntimeError("Field '{0}' with incorect size.".format(i))
            parsed_data.append((i, cls(_data, desc, i, self._message)))

        return parsed_data

    @property
    def fields(self):
        return self._fields


class PIDSegment(Segment):
    _identifier = "PID"
    _definition = [
        # (seq, len, field, opt, desc)
        (0, 4, "SI", "O", "setid - pid"),
        (1, 20, "CX", "B", "patient id"),
        (2, 20, "CX", "R", "patient identifier list"),
        (3, 20, "CX", "B", "alternate patient id"),
        (4, 48, "XPN", "R", "patient name"),
        (5, 48, "XPN", "O", "mothers maiden name"),
        (6, 26, "TS", "O", "date/time of birth"),
        (7, 1, "IS", "O", "sex"),
        (8, 48, "XPN", "O", "patient alias"),
        (9, 80, "CE", "O", "race"),
        (10, 106, "XAD", "O", "patient address"),
        # TODO: incomplete
    ]


class Header(Segment):
    _identifier = "MSH"

    _definition = [
        (0, 1, "ST", "R", "Field separator"),
        (1, 4, "ST", "R", "Encoding characters"),
        (2, 180, "HD", "O", "Sending application"),
        (3, 180, "HD", "O", "Sending facility"),
        (4, 180, "HD", "O", "Receiving application"),
        (5, 180, "HD", "O", "Receiving facility"),
        (6, 26, "TS", "O", "Date/Time of message"),
        (7, 40, "ST", "O", "Secirity"),
        (8, 7, "CM", "R", "Message type"),
        (9, 20, "ST", "R", "Message control id"),
        (10, 3, "PT", "R", "Processing id"),
        (11, 60, "VID", "R", "Version id"),
        # TODO: incomplete
    ]
