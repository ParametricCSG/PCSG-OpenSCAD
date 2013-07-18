#!/usr/bin/python3.3
import pcsg_openscad
import unittest

class TestUtilities(unittest.TestCase):

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
        expect = [1, 0, 0]
        self.assertEqual(expect, self.eng.makeBinaryList(vect))

    def test_applyCentering1(self):
        extrema = [10, 5, 6]
        centering = [True, True, True]
        default = [False, False, False]
        expect = "translate(v=[-5.0, -2.5, -3.0])"
        self.assertEqual(expect, self.eng.applyCentering(centering = centering,
                         extrema = extrema, default = default))

    def test_applyCentering2(self):
        extrema = [5, 5, 10]
        centering = [True, True, True]
        default = [True, True, False]
        expect = "translate(v=[0, 0, -5.0])"
        self.assertEqual(expect, self.eng.applyCentering(centering = centering,
                         extrema = extrema, default = default))

    def test_applyCentering3(self):
        extrema = [5, 5, 10]
        centering = [False, False, False]
        default = [True, True, False]
        expect = "translate(v=[2.5, 2.5, 0])"
        self.assertEqual(expect, self.eng.applyCentering(centering = centering,
                         extrema = extrema, default = default))

    def test_applyCentering4(self):
        extrema = [3, 3, 3]
        centering = [True, True, True]
        default = [True, True, True]
        expect = ""
        self.assertEqual(expect, self.eng.applyCentering(centering = centering,
                         extrema = extrema, default = default))

    def test_applyCentering5(self):
        extrema = [3, 3, 3]
        centering = [False, False, True]
        default = [True, True, True]
        expect = "translate(v=[1.5, 1.5, 0])"
        self.assertEqual(expect, self.eng.applyCentering(centering = centering,
                         extrema = extrema, default = default))
if __name__ == '__main__':
    unittest.main()

