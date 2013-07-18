#!/usr/bin/python3.3
import pcsg_openscad
import unittest

class TestTransformations(unittest.TestCase):

    def setUp(self):
        self.eng = pcsg_openscad.OpenSCADEngine()

    def test_translate1(self):
        vect = [1, 2, 3]
        expect = "translate(v=[1, 2, 3])"
        self.assertEqual(expect, self.eng.translate(vect))

    def test_translate2(self):
        vect = [1.203, 0.100000, 1.02]
        expect = "translate(v=[1.203, 0.1, 1.02])"
        self.assertEqual(expect, self.eng.translate(vect))

    def test_translate3(self):
        vect = [0, 0, 0]
        expect = ""
        self.assertEqual(expect, self.eng.translate(vect))

    def test_minkowski(self):
        self.assertEqual("minkowski()", self.eng.minkowski())
    
    def test_hull(self):
        self.assertEqual("hull()", self.eng.hull())

    def test_union(self):
        self.assertEqual("union()", self.eng.union())

    def test_difference(self):
        self.assertEqual("difference()", self.eng.difference())

    def test_intersection(self):
        self.assertEqual("intersection()", self.eng.intersection())

    def test_rotate1(self):
        rotation = {'angle': 45, 'axis': [1, 0, 0]}
        expect = "rotate(a=45, v=[1, 0, 0])"
        self.assertEqual(expect, self.eng.rotate(rotation))

    def test_rotate2(self):
        rotation = {'angle': 60, 'axis': [0, True, True]}
        expect = "rotate(a=60, v=[0, 1, 1])"
        self.assertEqual(expect, self.eng.rotate(rotation))

    def test_rotate3(self):
        rotation = {'angle': 60, 'axis': [False, False, False]}
        expect = ""
        self.assertEqual(expect, self.eng.rotate(rotation))

    def test_mirror1(self):
        vect = [True, False, True]
        expect = "mirror([1, 0, 1])"
        self.assertEqual(expect, self.eng.mirror(vect))

    def test_mirror2(self):
        vect = [0, 0, 1]
        expect = "mirror([0, 0, 1])"
        self.assertEqual(expect, self.eng.mirror(vect))

    def test_mirror3(self):
        vect = []
        expect = ""
        self.assertEqual(expect, self.eng.mirror(vect))

    def test_scale1(self):
        vect = [0.5, 0.501, 10]
        expect = "scale(v=[0.5, 0.501, 10])"
        self.assertEqual(expect, self.eng.scale(vect))

    def test_scale2(self):
        vect = []
        expect = ""
        self.assertEqual(expect, self.eng.scale(vect))

    def test_resize(self):
        resizer = {'newsize': [10, 30, 40], 'auto': [True, False, True]}
        expect = "resize(newsize=[10, 30, 40], auto=[true, false, true])"
        self.assertEqual(expect, self.eng.resize(resizer))

    def test_multmatrix1(self):
        matrix = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
        expect = "multmatrix(m=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])"
        self.assertEqual(expect, self.eng.multmatrix(matrix))

    def test_multmatrix2(self):
        matrix = []
        expect = ""
        self.assertEqual(expect, self.eng.multmatrix(matrix))

    def test_color1(self):
        color = [0.5, 0.1, 0.4]
        expect = "color([0.5, 0.1, 0.4])"
        self.assertEqual(expect, self.eng.color(color))

    def test_color1(self):
        color = []
        expect = ""
        self.assertEqual(expect, self.eng.color(color))

if __name__ == '__main__':
    unittest.main()

