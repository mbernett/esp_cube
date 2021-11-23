#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import datetime
import time
#import argparse
import matplotlib.pyplot as plt

#Backup
#parser = argparse.ArgumentParser()
#parser.add_argument("-l", "--lato", help="Lato della Box",type=int)
#parser.add_argument("-p", "--points", help="Number of Points",type=int)
#parser.add_argument("-o", "--output", help="Output")
#args = parser.parse_args()
#lato_box=args.lato
#npoints=args.points

bohr=0.529177249 # bohr to angstrom


input_file=input("Please insert a PDB file: ")
#lato_box=int(input("Please insert box side: "))
npoints=int(input("Please inser # points: "))
output=input("path output: ")

lato_box=10
xmin=lato_box*bohr;
xmax=-xmin
xinc=-(xmax-xmin)/(npoints-1);
spacing=xinc/bohr # spacing

class Atoms:
    def __init__(self,x,y,z,charge):
        self.x=x
        self.y=y
        self.z=z
        self.charge=charge


with open(input_file) as file:
    atoms = []
    for line in file:
        fields = line.strip().split()
        if fields[0]=='ATOM':
            x=float(fields[5])
            y=float(fields[6])
            z=float(fields[7])
            charge=float(fields[8])
            atoms.append(Atoms(x,y,z,charge))
        else:
            pass

#griglia
X = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints) # min, max, npoints
Y = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints)
Z = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints)


xx, yy, zz = np.meshgrid(X,Y,Z)

#calcolo

iterator=0
for i in atoms:
    if iterator==0:
        a=i.charge/np.sqrt((xx.flatten()-i.x)**2+(yy.flatten()-i.y)**2+(zz.flatten()-i.z)**2)
        iterator=+1
    else:
        a=a+i.charge/np.sqrt((xx.flatten()-i.x)**2+(yy.flatten()-i.y)**2+(zz.flatten()-i.z)**2)
    
a=a.reshape(100,-1)

a=a.reshape(-1,npoints)

fmt=np.array(['  %3.4e'] *npoints)
fmt

fmt2=""
iterator=1
for i in fmt:
    fmt2=fmt2+str(i)
    if iterator % 6 == 0:
        fmt2=fmt2+str('\n')
    iterator=iterator+1

spacing=format(spacing, '.5f')
lato_box=format(lato_box, '.5f')

header=""" Opt job potenital=scf
Electrostatic potential from Total SCF Density
    {}  -{}   -{}   -{}
    {}   {}     0.00000     0.00000
    {}   0.00000     {}     0.00000
    {}   0.00000     0.00000     {}""".format(len(atoms),lato_box,lato_box,lato_box,npoints,spacing,npoints,spacing,npoints,spacing)
for i in atoms:
    primo=format(i.x/bohr, '.5f')
    secondo=format(i.y/bohr, '.5f')
    terzo=format(i.z/bohr, '.5f')
    header=header+"\n    0    0.00000     {}     {}    {}".format(primo,secondo,terzo)

np.savetxt('{}'.format(output),a,fmt=fmt2,header=header,comments='')




