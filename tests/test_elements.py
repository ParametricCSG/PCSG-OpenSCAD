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

    def test_cylinder1(self):
        datas = {'radius': 4, 'height': 5, 'center':[True,True,False]}
        expect = "cylinder(r=4, h=5, $fn=80);"
        self.assertEqual(expect, self.eng.cylinder(datas))

    def test_cylinder2(self):
        datas = {'radius': 10, 'height': 20, 'center':[False,False,False]}
        expect = "translate(v=[5.0, 5.0, 0])cylinder(r=10, h=20, $fn=200);"
        self.assertEqual(expect, self.eng.cylinder(datas))

    def test_cylinder3(self):
        datas = {'radius': 8, 'height': 5, 'center':[True,False,True]}
        expect = "translate(v=[0, 4.0, -2.5])cylinder(r=8, h=5, $fn=160);"
        self.assertEqual(expect, self.eng.cylinder(datas))

    def test_sphere1(self):
        datas = {'radius': 4, 'center':[True,True,True]}
        expect = "sphere(r=4, $fn=80);"
        self.assertEqual(expect, self.eng.sphere(datas))

    def test_sphere2(self):
        datas = {'radius': 10, 'center':[False,False,False]}
        expect = "translate(v=[5.0, 5.0, 5.0])sphere(r=10, $fn=200);"
        self.assertEqual(expect, self.eng.sphere(datas))

    def test_sphere3(self):
        datas = {'radius': 8, 'center':[True,False,True]}
        expect = "translate(v=[0, 4.0, 0])sphere(r=8, $fn=160);"
        self.assertEqual(expect, self.eng.sphere(datas))

if __name__ == '__main__':
    unittest.main()
