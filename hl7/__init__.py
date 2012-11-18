# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import io

from .defaults import SEGMENT_SEPARATOR, SECTION_SEPARATOR, FIELD_SEPARATOR
from . import fields, segments


class Message(object):
    header_cls = segments.Header

    _header = None
    _segments = None

    def __init__(self, message):
        if not isinstance(message, bytes):
            message = message.encode('utf-8')

        self._message = message.split(SEGMENT_SEPARATOR)
        self._parse_header()

    def _parse_header(self):
        return self.header_cls(self._message[0], self)

    @property
    def header(self):
        if self._header is None:
            self._header = self._parse_header()
        return self._header


def parse(data=None, filename=None, cls=Message):
    if filename is not None:
        with io.open(filename, "rb") as f:
            return cls(f.read())

    raise RuntimeError
