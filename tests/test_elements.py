#!/usr/bin/python3.3
import pcsg_openscad
import unittest

class TestElements(unittest.TestCase):

    def setUp(self):
        self.eng = pcsg_openscad.OpenSCADEngine()

    def test_cube1(self):
        datas = {'center': [True,True,True], 'size': [10,20,30]}
        expect = "translate(v=[-5.0, -10.0, -15.0])cube(size=[10, 20, 30]);"
        self.assertEqual(expect, self.eng.cube(datas))

    def test_cube2(self):
        datas = {'center': [True,False,True], 'size': [2,4,3]}
        expect = "translate(v=[-1.0, 0, -1.5])cube(size=[2, 4, 3]);"
        self.assertEqual(expect, self.eng.cube(datas))

    def test_cube3(self):
        datas = {'center': [False,False,False], 'size': [50,20,30]}
        expect = "cube(size=[50, 20, 30]);"
        self.assertEqual(expect, self.eng.cube(datas))
if __name__ == '__main__':
    unittest.main()
