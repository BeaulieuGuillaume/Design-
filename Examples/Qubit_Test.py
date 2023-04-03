# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 16:02:00 2022

@author: beaulieu
"""


import numpy as np
import gdspy
from GDS import Qubit




lib = gdspy.GdsLibrary()
gdspy.current_library = lib


Chipcell=lib.new_cell("Xmon")

GroundPlaneLayer=1
StripWidth=24
SlotWidth=24
CrossLength=354

Qubit=Qubit.Xmon(0,0,0,3)
Qubit.setParameters(StripWidth, SlotWidth, CrossLength)



#Parameters U Patch
SideWidth=4.75
BottomHeight=3
RadiusCorner=0.5
SideHeight=11.66
TotalWidth=15
Overlap=0
TerminationUPatch={"UPatch":[SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth,Overlap]}


#Parameters of the TPATCH
TotalWidth=10
PartialHeight=5.62
TopWidth=5
RadiusCorner=0.5
TotalHeight=12.08
TopHeight=1.5
TerminationTPatch={"TPatch":[TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight]}


#Parameters of the JJ
SmallWidth=0.5
LargeWidth=0.232
RestrictedLength=5
TotalLength=14
LeftJunctionX=6
RightJunctionX=4
DisplacementY=1
LayerUnderCut=5
TerminationSQUID={"SQUIDDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY]}
TerminationJunction={"JunctionDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY]}
TerminationSQUIDUnderCut={"SQUIDDoubleAngleJunctionUnderCut":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY,LayerUnderCut]}






Design=Qubit.draw()

Design=Qubit.drawTermination(TerminationTPatch, "+y", 6)
Design=Qubit.drawTermination(TerminationSQUIDUnderCut, "+y", 6)
Design=Qubit.drawTermination(TerminationUPatch, "+y", 6)
Design=Qubit.drawTermination(TerminationTPatch, "-y", 6)
Design=Qubit.drawTermination(TerminationSQUIDUnderCut, "-y", 6)
Design=Qubit.drawTermination(TerminationUPatch, "-y", 6)
Design=Qubit.drawTermination(TerminationTPatch, "+x", 6)
Design=Qubit.drawTermination(TerminationSQUIDUnderCut, "+x",6)
Design=Qubit.drawTermination(TerminationUPatch, "+x", 6)
Design=Qubit.drawTermination(TerminationTPatch, "-x", 6)
Design=Qubit.drawTermination(TerminationSQUIDUnderCut, "-x",6)
Design=Qubit.drawTermination(TerminationUPatch, "-x", 6)




Chipcell.add(Design)






lib.write_gds('Qubit.gds')
