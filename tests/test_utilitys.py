#!/usr/bin/python3.3
import pcsg_openscad
import unittest

class TestTransformations(unittest.TestCase):

    def setUp(self):
        self.eng = pcsg_openscad.OpenSCADEngine()

    def test_makeBool1(self):
        val = True
        expect = "true"
        self.assertEqual(expect, self.eng.makeBool(val))

    def test_makeBool2(self):
        vect = [True, False, False]
        expect = "[true, false, false]"
        self.assertEqual(expect, self.eng.makeBool(vect))

    def test_isAllZeros1(self):
        vect = [0, 1, 0]
        expect = False
        self.assertEqual(expect, self.eng.isAllZeros(vect))

    def test_isAllZeros2(self):
        vect = [0, 0, 0]
        expect = True
        self.assertEqual(expect, self.eng.isAllZeros(vect))

    def test_makeBinaryList1(self):
        vect = [True, False, False]
        expect = "[1, 0, 0]"
        self.assertEqual(expect, self.eng.makeBinaryList(vect))

if __name__ == '__main__':
    unittest.main()

