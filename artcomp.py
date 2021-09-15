#!/usr/bin/python

import subprocess
import os
import random 
import sys


import toml


tomld = toml.load(open("config.txt"))
#print d["global"]["chop"]
#print d["colors"]
#sys.exit()

#subprocess.call(["ls", "-l"])


colors = tomld["colors"].keys();
cansize = tomld["global"]["size"]
canchop = tomld["global"]["chop"]
rotate = tomld["global"]["rotate"]
scale = tomld["global"]["scale"]
canborder = cansize;
if (canchop):
     canborder = 0

def findpng(dir):
    files = subprocess.check_output(["find", dir, "-name", "*.png", "-print0"])
    farray = list(filter(lambda x: x != "", files.split('\0')))
    return farray


def placepics(prefix, pics, locs, cols, count): 
    cmd = ""
    for i in range(0, count):
        # get random file from directory 
        x = random.choice(pics)
        pics.remove(x)
        geom = random.choice(locs)
        locs.remove(geom)
        color = random.choice(cols)
        cols.remove(color)
        sc = random.randint(scale[0] * 100, scale[1] * 100)
        rot = random.randint(rotate[0], rotate[1])
        tilefile = prefix + str(i) + ".png"
        tcmd = str("convert -background none '" + x + "' " 
            + "-matte \( +clone -fuzz 50% -transparent lime \) -compose DstOut -composite " 
            + "-trim +repage -fuzz 90% -fill '" + color + "' -opaque white " 
            + "-scale " + str(sc) + "% " 
            + "-rotate " + str(rot) + " "
            + " '" + tilefile + "' ")
        print tcmd
        os.system(tcmd)
        x = geom[0] + canborder
        y = geom[1] + canborder 
        cmd = cmd + " '" + tilefile + "' -gravity NorthEast -geometry %+d%+d" % (x,y) + " -composite " 
    return cmd

random.seed()
cmd = str("convert -size %dx%d canvas:white " % (cansize + canborder*2, cansize + canborder*2))

for xd in tomld["directory"]:
    print xd["name"]
    cmd = cmd + " " + placepics(xd["name"], findpng(xd["name"]), xd["locations"], colors, xd["choose"])  
 
cmd = cmd + " -trim +repage -resize 2048x2048! +repage " + sys.argv[1]

print cmd
os.system(cmd)
    

