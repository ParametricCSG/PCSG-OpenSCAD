#! /usr/bin/python3
import argparse
import sys
import json
import os
import subprocess
import math


class OpenSCADEngine:
    """
    Operation:
    Evaluate and regenerate JSON tree by order...
    required elements, parameters,
    parameter operations, elements, element operations
    """
    def __init__(self):
        self.level = 0
        self.output = ""
        self.operations = ["union", "difference", "intersection", "hull",
                           "translate", "rotate", "minkowski", "mirror",
                           "resize", "scale"]
        self.elements = ["cube", "cylinder", "sphere", "cone", "ntube", "hole"]

    def parseJSON(self, data):
        output = ""
        if data['category']:
            if data['category'] == "operation":
                if data['name'] in self.operations:
                    scadOperation = self.parseOperation(data) + "{\n"
                    output += " " * self.level * args.indent + scadOperation
                    for types in data['elements']:
                        self.level += 1
                        output += self.parseJSON(types)
                        output += "\n"
                        self.level -= 1
                    output += " " * self.level * args.indent + "}\n"
                    return output
                else:
                    a = "echo("+data['name']+");"
                    self.output += a
                    self.parseJSON(data['construction'])
            if data['category'] == "element":
                props = self.parseProperties(data)
                output += " " * self.level * args.indent + props
                if data['name'] in self.elements:
                    output += self.parseElement(data)
                    return output
                elif self.level == 0:
                    print("Found element '" + data['name'] + "' at top level")
                    print("Traversing to construction")
                    output += self.parseJSON(data['construction'])
                    return output
                else:
                    print("Found element '" + data['name']
                          + "' at level " + str(self.level))
                    print("Traversing to construction.")
                    output += self.parseJSON(data['construction'])
                    return output

    def parseOperation(self, data):
        """
        Parse an operation and return an OpenSCAD equivalent
        """
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
        if 'highlight' in data:
            tempStr += self.highlight()
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
            tempStr += self.ntube(data)
        elif data['name'] == "cone":
            tempStr += self.cone(data)
        elif data['name'] == "hole":
            tempStr += self.hole(data)
        return tempStr

    def makeBool(self, pyBool):
        """
        Args: List of booleans
        Returns: an OpenSCAD compatible bool string
        """
        return str(pyBool).lower()

    def isAllZeros(self, vector):
        return all(v == 0 for v in vector)

    def makeBinaryList(self, vector):
        """If a value is true/false in a list make it 1/0"""
        return list(map(int, vector))

    def applyCentering(self,
                       centering,
                       extrema,
                       default=[False, False, False]
                       ):
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
        return radius * math.cos(math.pi / sides)

    def radiusFromApothem(self, apothem, sides):
        return apothem / math.cos(math.pi / sides)

    def hole(self, data):
        tempStr = ""
        sides = self.holeSides(data['radius'])
        radius = self.radiusFromApothem(apothem=data['radius'],
                                        sides=sides)
        if 'tolerance' in data:
            radius += data['tolerance']
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=[radius, radius,
                                                data['height']],
                                       default=[True, True, False])
        tempStr += "cylinder(r=" + str(radius) + ", h=" + str(data['height']) \
                   + ", $fn=" + str(sides)+");"
        return tempStr

    def ntube(self, data):
        tempStr = ""
        sides = data['sides']
        radius = self.radiusFromApothem(apothem=data['apothem'], sides=sides)
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=[radius, radius,
                                                data['height']],
                                       default=[True, True, False])
        tempStr += "cylinder(r="+str(radius) + ", h="+str(data['height']) \
                   + ", $fn=" + str(sides)+");"
        return tempStr

    def cone(self, data):
        """
        Returns an OpenSCAD cylinder string
        """
        tempStr = ""
        maxRadius = max([data['topRadius'], data['bottomRadius']])
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=[maxRadius,
                                                maxRadius,
                                                data['height']],
                                       default=[True, True, False])
        tempStr += "cylinder(r1=" + str(data['bottomRadius']) + ", r2=" \
                   + str(data['topRadius']) + ", h=" + str(data['height']) \
                   + ", $fn=" + str(maxRadius*20) + ");"
        return tempStr

    def cube(self, data):
        """
        Returns an OpenSCAD cube string
        """
        tempStr = ""
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=data['size'],
                                       default=[False, False, False])
        tempStr += "cube(size=" + str(data['size']) + ");"
        return tempStr

    def sphere(self, data):
        """
        Returns an OpenSCAD sphere string
        """
        tempStr = ""
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=[data['radius']]*3,
                                       default=[True, True, True])
        tempStr += "sphere(r=" + str(data['radius']) \
                   + ", $fn=" + str(data['radius']*20) + ");"
        return tempStr

    def cylinder(self, data):
        """
        Returns an OpenSCAD cylinder string
        """
        tempStr = ""
        tempStr += self.applyCentering(centering=data['center'],
                                       extrema=[data['radius'],
                                                data['radius'],
                                                data['height']],
                                       default=[True, True, False])
        tempStr += "cylinder(r=" + str(data['radius']) + ", h=" \
                   + str(data['height']) + ", $fn=" \
                   + str((data['radius'])*20) + ");"
        return tempStr

    def rotate(self, rotation):
        cleanedAxis = self.makeBinaryList(rotation['axis'])
        if self.isAllZeros(cleanedAxis):
            return ""
        else:
            return "rotate(a=" + str(rotation['angle']) + ", v=" \
                   + str(cleanedAxis) + ")"

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
        return "resize(newsize=" + str(resize['newsize']) \
               + ", auto=" + cleanedAuto + ")"

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

    def highlight(self):
        return "#"

if __name__ == "__main__":
    #Setup Command line arguments
    parser = argparse.ArgumentParser(prog="textcad",
                                     usage="%(prog)s [options] input...",
                                     description="The textcad engine."
                                     )
    parser.add_argument("-o", "--output", nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="Output file, defaults to stdout"
                        )
    parser.add_argument("input", nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="input file, defaults to stdin"
                        )
    parser.add_argument("-v", "--verbose",
                        type=bool,
                        help="verbose output while traversing textcad file"
                        )
    parser.add_argument("-s", "--show",
                        action='store_true',
                        default=False,
                        help="launch OpenSCAD with the file when finished"
                        )
    parser.add_argument("-i", "--indent",
                        type=int,
                        default=4,
                        help="number of spaces for indentation (default: 4)"
                        )
    parser.add_argument('--version',
                        action='version',
                        version="%(prog)s 0.0.1-dev"
                        )

    #Always output help by default
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)  # Exit after help display

    args = parser.parse_args()

    j = json.loads(args.input.read())
    c = OpenSCADEngine()
    c.output = c.parseJSON(j)
    args.output.write(c.output)
    if args.show:
        subprocess.Popen(["openscad", os.path.abspath(args.output.name)])
