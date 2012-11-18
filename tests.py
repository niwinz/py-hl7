# -*- coding: utf-8 -*-

import unittest
import pdb
import hl7
import hl7.segments


class TestPIDSegment(unittest.TestCase):
    def setUp(self):
        self.data = ("PID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ"
                     "|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35 209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMIN"
                     "GHAM^AL^35200^^O |||||||0105I30001^^^99DEF^AN")

    def test_parse_01(self):
        segment = hl7.segments.PIDSegment(self.data.encode('utf-8'), None)

        # Sex field
        index, field = segment.fields[7]

        self.assertEqual(field.description, "sex")
        self.assertEqual(field.value, b"M")


class TestMessageHeader(unittest.TestCase):
    def setUp(self):
        self.data = "MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4"

    def test_parse_01(self):
        segment = hl7.segments.Header(self.data.encode("utf-8"), None)

        index, field = segment.fields[4]
        self.assertEqual(field.value, b"BLDG4")

        #(Pdb) segment.fields[0][1].value
        #b'^~\\&'
        #(Pdb) segment.fields[2][1].value
        #b'ELAB-3'
        #(Pdb) segment.fields[3][1].value
        #b'GHH OE'
        #(Pdb) segment.fields[4][1].value
        #b'BLDG4'
        #(Pdb) segment.fields[4][1].value
        #b'BLDG4'
        #(Pdb) segment.fields[6][1].value
        #b''
        #(Pdb) segment.fields[7][1].value
        #b'ORU^R01'
