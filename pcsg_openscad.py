#! /usr/bin/python3.3
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import sys
import json
import os
import subprocess
import math

'''
Operation:
Evaluate and regenerate JSON tree by order...
required elements, parameters, parameter operations, elements, element operations
'''

class OpenSCADEngine:
    def __init__(self):
        self.level = 0
        self.output = ""
        self.operations = ["union", "difference", "intersection", "hull",
                           "translate", "rotate", "minkowski", "mirror", "resize",
                           "scale"]
        self.elements = ["cube", "cylinder", "sphere", "cone", "ntube", "hole"]

    def parseJSON(self, data):
        if data['category']:
            if data['category'] == "operation":
                if data['name'] in self.operations:
                    scadOperation = self.parseOperation(data) + "{"
                    self.output += " " * self.level * args.indent + scadOperation
                    for types in data['elements']:
                        self.level += 1
                        self.parseJSON(types)
                        self.output += "\n"
                        self.level -= 1
                    self.output += " " * self.level * args.indent + "}\n"
                else:
                    a = "echo("+data['name']+");"
                    self.output += a
                    self.parseJSON(data['construction'])
            if data['category'] == "element":
                props = self.parseProperties(data)
                self.output += " " * self.level * args.indent + props
                if data['name'] in self.elements:
                    self.output += self.parseElement(data)
                else:
                    print("Found top level element " + data['name'])
                    print("Unrecognized by the parser... traversing to construction")
                    self.parseJSON(data['construction'])

    def parseOperation(self, data):
        """Parse an operation and generate an OpenSCAD equivalent"""
        tempStr = self.parseProperties(data)
        if data['name'] == "translate":
            tempStr += self.translate(data['location'])
        elif data['name'] == "rotate":
            tempStr += self.rotate(data)
        elif data['name'] == "union":
            tempStr += self.union()
        elif data['name'] == "difference":
            tempStr += self.difference()
        elif data['name'] == "intersection":
            tempStr += self.intersection()
        elif data['name'] == "mirror":
            tempStr += self.mirror(data['axis'])
        elif data['name'] == "scale":
            tempStr += self.scale(data['multiplier'])
        elif data['name'] == "resize":
            tempStr += self.resize(data)
        elif data['name'] == "hull":
            tempStr += self.hull()
        elif data['name'] == "minkowski":
            tempStr += self.minkowski()
        return tempStr

    def parseProperties(self, data):
        tempStr = ""
        if 'color' in data:
            tempStr += self.color(data['color'])
        if 'location' in data:
            tempStr += self.translate(data['location'])
        if 'rotation' in data:
            tempStr += self.rotate(data['rotation'])
        if 'scale' in data:
            tempStr += self.scale(data['scale'])
        return tempStr

    def parseElement(self, data):
        tempStr = ""
        if data['name'] == "cube":
            tempStr += self.cube(data)
        elif data['name'] == "sphere":
            tempStr += self.sphere(data)
        elif data['name'] == "cylinder":
            tempStr += self.cylinder(data)
        elif data['name'] == "ntube":
            tempStr += self.nTube(data)
        elif data['name'] == "cone":
            tempStr += self.cone(data)
        elif data['name'] == "hole":
            tempStr += self.hole(data)
        return tempStr

    def makeBool(self, pyBool):
        """Takes a Python bool (type, or list of bools) and returns an OpenSCAD bool string"""
        return str(pyBool).lower()

    def isAllZeros(self, vector):
        return all( v == 0 for v in vector)

    def makeBinaryList(self, vector):
        """If a value is true/false in a list make it 1/0"""
        return list(map(int, vector))

    def applyCentering(self, centering, extrema, default=[False,False,False]):
        """Returns a translationg statement to apply centering by axis"""
        vect = [0, 0, 0]
        for idx, val in enumerate(centering):
            if val and not default[idx]:
                vect[idx] = -extrema[idx]/2
            elif not val and default[idx]:
                vect[idx] = extrema[idx]/2
        return self.translate(vect)

    def holeSides(self, radius):
        return max([math.floor(4*radius), 3])

    def apothem(self, radius, sides):
        return radius / math.cos(math.pi/ sides)

    def hole(self, data):
        tempStr = ""
        sides = self.holeSides(data['radius'])
        radius = 0.1 + self.apothem(radius = data['radius'], sides = sides)
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = [radius,
                                                  radius,
                                                  data['height']],
                                       default = [True,True,False])
        tempStr += "cylinder(r="+str(radius)+", h="+str(data['height'])+", $fn="+\
                    str(sides)+");"
        return tempStr

    def nTube(self, data):
        tempStr = ""
        sides = data['sides']
        radius = self.apothem(radius = data['width'], sides = sides)
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = [radius, radius,
                                                  data['height']],
                                       default = [True,True,False])
        tempStr += "cylinder(r="+str(radius)+", h="+str(data['height'])+", $fn="+\
                    str(sides)+");"
        return tempStr

    def cone(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Cube string"""
        tempStr = ""
        maxRadius = max([data['topRadius'], data['bottomRadius']])
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = [maxRadius,
                                                  maxRadius,
                                                  data['height']],
                                       default = [True,True,False])
        tempStr += "cylinder(r1=" + str(data['bottomRadius']) +", r2=" + \
                    str(data['topRadius']) + ", h=" + str(data['height']) + \
                    ", $fn=" + str(maxRadius*20) + ");"
        return tempStr

    def cube(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Cube string"""
        tempStr = ""
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = data['size'],
                                       default = [False,False,False])
        tempStr += "cube(size=" + str(data['size']) + ");"
        return tempStr

    def sphere(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Sphere string"""
        tempStr = ""
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = [data['radius']]*3,
                                       default = [True,True,True])
        tempStr += "sphere(r=" + str(data['radius']) + ", $fn=" + str(data['radius']*20) + ");"
        return tempStr

    def cylinder(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Cube string"""
        tempStr = ""
        tempStr += self.applyCentering(centering = data['center'],
                                       extrema = [data['radius'],
                                                  data['radius'],
                                                  data['height']],
                                       default = [True,True,False])
        tempStr += "cylinder(r=" + str(data['radius']) + ", h=" + str(data['height']) \
              + ", $fn=" + str((data['radius'])*20) + ");"
        return tempStr

    def rotate(self, rotation):
        cleanedAxis = self.makeBinaryList(rotation['axis'])
        if self.isAllZeros(cleanedAxis):
            return ""
        else:
            return "rotate(a=" + str(rotation['angle']) + ", v=" + \
                         str(cleanedAxis) + ")"

    def translate(self, location):
        if self.isAllZeros(location):
            return ""
        else:
            return "translate(v=" + str(location) + ")"

    def scale(self, multiplier):
        if multiplier:
            return "scale(v=" + str(multiplier) + ")"
        else:
            return ""

    def resize(self, resize):
        cleanedAuto = self.makeBool(resize['auto'])
        return "resize(newsize=" + str(resize['newsize']) + ", auto=" + cleanedAuto + ")"

    def mirror(self, axis):
        if axis:
            cleanedAxis = self.makeBinaryList(axis)
            return "mirror(" + str(cleanedAxis) + ")"
        else:
            return ""

    def multmatrix(self, matrix):
        if matrix:
            return "multmatrix(m=" + str(matrix) + ")"
        else:
            return ""

    def color(self, color):
        if color:
            return "color(" + str(color) + ")"
        else:
            return ""

    def minkowski(self):
        return "minkowski()"

    def hull(self):
        return "hull()"

    def union(self):
        return "union()"

    def difference(self):
        return "difference()"

    def intersection(self):
        return "intersection()"

if __name__=="__main__":
    #Setup Command line arguments
    parser = argparse.ArgumentParser(
        prog = "pcsg-openscad",
        usage = "%(prog)s [options] input...",
        description = "An engine for PCSG using OpenSCAD."
        )
    parser.add_argument("-o", "--output", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help = "Output file, defaults to stdout")
    parser.add_argument("input", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help = "Input file, defaults to stdin")
    parser.add_argument("-v", "--verbose", type=bool, help="verbose output while traversing PCSG file")
    parser.add_argument("-s", "--show", action='store_true', default=False, help="launch OpenSCAD with the file when finished")
    parser.add_argument("-i", "--indent", type=int, default=4, help="set number of spaces for indentation (default: 4)")
    parser.add_argument('--version', action='version', version="%(prog)s 0.0.1-dev")

    #Always output help by default
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0) # exit after help display

    args = parser.parse_args()

    j = json.loads(args.input.read())
    c = OpenSCADEngine()
    c.parseJSON(j)
    args.output.write(c.output)
    if args.show:
        subprocess.Popen(["openscad", os.path.abspath(args.output.name)])
