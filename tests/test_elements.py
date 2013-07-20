#!/usr/bin/python3.3
import textcad_engine
import unittest

class TestElements(unittest.TestCase):

    def setUp(self):
        self.eng = textcad_engine.OpenSCADEngine()

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

    def test_ntube1(self):
        datas = {'apothem': 4, 'sides': 6, 'height': 5, 'center':[True,True,False]}
        expect = "cylinder(r=4.618802153517006, h=5, $fn=6);"
        self.assertEqual(expect, self.eng.ntube(datas))

    def test_ntube2(self):
        datas = {'apothem': 10, 'sides': 12, 'height': 12, 'center':[True,False,False]}
        expect = "translate(v=[0, 5.176380902050415, 0])cylinder(r=10.35276180410083, h=12, $fn=12);"
        self.assertEqual(expect, self.eng.ntube(datas))

    def test_ntube3(self):
        datas = {'apothem': 2, 'sides': 3, 'height': 4, 'center':[False,False,True]}
        expect = "translate(v=[1.9999999999999996, 1.9999999999999996, -2.0])cylinder(r=3.999999999999999, h=4, $fn=3);"
        self.assertEqual(expect, self.eng.ntube(datas))

    def test_cone1(self):
        datas = {'topRadius': 4, 'bottomRadius': 5, 'height': 5, 'center':[True,True,False]}
        expect = "cylinder(r1=5, r2=4, h=5, $fn=100);"
        self.assertEqual(expect, self.eng.cone(datas))

    def test_cone2(self):
        datas = {'topRadius': 4, 'bottomRadius': 5, 'height': 5, 'center':[False,False,False]}
        expect = "translate(v=[2.5, 2.5, 0])cylinder(r1=5, r2=4, h=5, $fn=100);"
        self.assertEqual(expect, self.eng.cone(datas))

    def test_cone3(self):
        datas = {'topRadius': 4, 'bottomRadius': 3, 'height': 5, 'center':[False,False,True]}
        expect = "translate(v=[2.0, 2.0, -2.5])cylinder(r1=3, r2=4, h=5, $fn=80);"
        self.assertEqual(expect, self.eng.cone(datas))

    def test_hole1(self):
        datas = {'radius': 3, 'height': 3, 'center':[True,False,True]}
        expect = "translate(v=[0, 1.6029142706151245, -1.5])cylinder(r=3.205828541230249, h=3, $fn=12);"
        self.assertEqual(expect, self.eng.hole(datas))

    def test_hole2(self):
        datas = {'radius': 10, 'height': 50, 'center':[True,True,False]}
        expect = "cylinder(r=10.130921984828255, h=50, $fn=40);"
        self.assertEqual(expect, self.eng.hole(datas))

    def test_hole3(self):
        datas = {'radius': 0.5, 'height': 2, 'center':[False,True,False]}
        expect = "translate(v=[0.5499999999999999, 0, 0])cylinder(r=1.0999999999999999, h=2, $fn=3);"
        self.assertEqual(expect, self.eng.hole(datas))

if __name__ == '__main__':
    unittest.main()
