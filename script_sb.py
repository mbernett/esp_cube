#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import datetime
import time
#import argparse
#import matplotlib.pyplot as plt

#parser = argparse.ArgumentParser()

#parser.add_argument("-l", "--lato", help="Lato della Box",type=int)
#parser.add_argument("-p", "--points", help="Number of Points",type=int)
#parser.add_argument("-o", "--output", help="Output")
#args = parser.parse_args()
#lato_box=args.lato
#npoints=args.points
bohr=0.529177249 # bohr to angstrom
input_file=input("Please insert a PDB file: ")
lato_box=int(input("Please insert box side: "))
npoints=int(input("Please decleare how many points you want to consider: "))
output=input("Output's name: ")

spacing=((lato_box*bohr)-(-lato_box*bohr))/9/bohr # spacing


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
        if fields[1]=='ATOM':
            x=float(fields[5])
            y=float(fields[6])
            z=float(fields[7])
            charge=float(fields[8])
            atoms.append(Atoms(x,y,z,charge))
        else:
            pass

X = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints) # min, max, npoints
Y = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints)
Z = np.linspace(-(lato_box)*bohr,lato_box*bohr,npoints)

xx, yy, zz = np.meshgrid(X,Y,Z)

print(xx.shape, yy.shape, zz.shape)

iterator=0
for i in atoms:
    if iterator==0:
        a=i.charge/np.sqrt((xx.flatten()-i.x)**2+(yy.flatten()-i.y)**2+(zz.flatten()-i.y)**2)
        iterator=+1
    else:
        a=a+i.charge/np.sqrt((xx.flatten()-i.x)**2+(yy.flatten()-i.y)**2+(zz.flatten()-i.y)**2)
    
fmt='  %3.4e' *npoints
fmt

spacing=format(spacing, '.5f')
lato_box=format(lato_box, '.5f')
# header: needs to be improved to print stuff consistently with the input
header=""" Opt job potenital=scf
 Electrostatic potential from Total SCF Density
    {}  -{}   -{}   -{}
   10    {}     0.00000     0.00000
   10    0.00000     {}     0.00000
   10    0.00000     0.00000     {}
    0    0.00000     0.00000     0.00000     0.00000""".format(len(atoms),lato_box,lato_box,lato_box,spacing,spacing,spacing)


print(header)

fmt2='\n'.join(fmt[i:i+42] for i in range (0,len(fmt),42))
#fmt='  %3.4e  %3.4e  %3.4e  %3.4e  %3.4e  %3.4e\n  %3.4e  %3.4e  %3.4e  %3.4e' # note the \n
# this is specidif to a grid with 10 points. Every 6 points there needs to be a \n.
# Best would be to automatize this.


# In[197]:


# print formatted, with header
np.savetxt('{}'.format(output),a.reshape(100,-1),fmt=fmt2,header=header,comments='')

