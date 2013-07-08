#! /usr/bin/env python
import argparse
import sys
import json
import os
import subprocess

'''
Operation:
Evaluate and regenerate JSON tree by order...
required elements, parameters, parameter operations, elements, element operations
'''
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
    sys.exit(0)
args = parser.parse_args()

class OpenSCADEngine:
    def __init__(self):
        self.level = 0
        self.output = ""
        self.operations = ["union", "difference", "intersection"]
        self.elements = ["cube", "cylinder", "sphere", "cone"]
        
    def parseJSON(self, data):
        if data['category']:
            if data['category'] == "operation":
                if data['name'] in self.operations:
                    a = data['name'] + "(){\n"                  
                    self.output += " " * self.level * args.indent + a
                    for types in data['elements']:
                        self.level += 1
                        self.parseJSON(types)
                        self.level -= 1
                    self.output += " " * self.level * args.indent + "}\n"
            if data['category'] == "element":
                if data['name'] in self.elements:
                    a = ""
                    if data['name'] == "cube":
                        a = self.makeCube(data)
                    if data['name'] == "sphere":
                        a = self.makeSphere(data)
                    if data['name'] == "cylinder":
                        a = self.makeCylinder(data)     
                    self.output += " " * self.level + a
                else:
                    sys.stderr.write("ERROR: Unknown element name\n")
				    
    def makeCube(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Cube string"""
        #apply centering
        for idx, val in enumerate(data['center']):
            if val:
                data['location'][idx] -= data['size'][idx]/2
        return "translate(" + str(data['location']) + ")cube(size=" + \
                str(data['size']) + ");\n"
   
    def makeSphere(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Sphere string"""
        #apply centering
        for idx, val in enumerate(data['center']):
            if not val:
                data['location'][idx] += data['radius']
        return "translate(" + str(data['location']) + ")sphere(r=" + \
                str(data['radius']) + ");\n"

    def makeCylinder(self, data):
        """Take a python dictionary and make an OpenSCAD compatible Cube string"""
        #apply centering
        for idx, val in enumerate(data['center']):
            if not val and idx in [0,1]: 
                data['location'][idx] += data['radius']
            elif val and idx == 2:
                data['location'][idx] -= data['height']/2
        return "translate(" + str(data['location']) + ")cylinder(r=" + \
                str(data['radius']) + ", h=" + str(data['height']) + ");\n"

            
j = json.loads(args.input.read())
c = OpenSCADEngine()
c.parseJSON(j)
args.output.write(c.output)
if args.show:
    subprocess.Popen(["openscad", os.path.abspath(args.output.name)])
