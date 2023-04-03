# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:54:15 2022

@author: beaulieu
"""

import numpy as np
import gdspy
from GDS import CPWGuide as CPW
from GDS import Qubit 

lib = gdspy.GdsLibrary()
gdspy.current_library = lib
ChipCell=lib.new_cell("ChipCell")

#%% Parameters for the CPW elements 


#Parameters for the Pads
StripWidth=16.692
SlotWidth=10
PadWidth=150.756
OffsetPadEtch=100
PadLength=200
ImpMatchLength=200
TerminationPad={"CPWPad":[PadWidth,OffsetPadEtch,PadLength,ImpMatchLength]}

#Qubit Coupling Parameters
CentralConductorWidth=100
SideConductorWidth=42
SideLength=144
TerminationQubitCoupling={"CPWQubitCoupling":[CentralConductorWidth,SideConductorWidth,SideLength]}

#CPW parameters
InitStripWidth=16.692
InitSlotWidth=10
FinStripWidth=5
FinSlotWidth=3.032
TaperedLength=10
StraightLength=288.484
TerminationQubitDrive={"CPWQubitDriveLine":[FinStripWidth,FinSlotWidth,TaperedLength,StraightLength]}

#Parameters for the Fluxline
InitStripWidth=16.471
InitSlotWidth=10
FinStripWidth=5
FinSlotWidth=3.032
TaperedLength=10
StraightLength=288.484
Gap=3
OpeningLength=21.5
OpeningOffset=5.5
TerminationFluxLine={"CPWFluxLine":[FinStripWidth, FinSlotWidth, TaperedLength, StraightLength, Gap, OpeningLength, OpeningOffset]}


#%% Parameters of the Qubit elements 
SideWidth=4.75
BottomHeight=3
RadiusCorner=0.5
SideHeight=11.66
TotalWidth=15
TerminationUPatch={"UPatch":[SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth]}


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
TerminationSQUID={"SQUIDDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY]}


#%% Makes the chip design
GroundPlaneLayer=1
PatchLayer=5
JJLayer=10

StripWidth=16.692
SlotWidth=10

WaveGuide=CPW.CPWGuide(0, 0, 0, GroundPlaneLayer)
WaveGuide.setParameters(StripWidth, SlotWidth)

#Creates the transmission line
Design=WaveGuide.drawTermination(TerminationPad, "-x", GroundPlaneLayer,Reversed=True)
Design=WaveGuide.drawStraight(5700, "+x")
Design=WaveGuide.drawTermination(TerminationPad, "+x", GroundPlaneLayer)

#Creates the redout resonator 
WaveGuide.SetPoint(1830, -70)
Design=WaveGuide.drawStraight(400, "+x")
Deisgn=WaveGuide.drawTurn(100, "r", "+x")
Design=WaveGuide.drawStraight(400, "-y")
Design=WaveGuide.drawTurn(100, "r", "-y")
Design=WaveGuide.drawStraight(750, "-x")
Design=WaveGuide.drawTurn(100, "ll", "-x")
Design=WaveGuide.drawStraight(750, "+x")
Design=WaveGuide.drawTurn(100, "rr", "+x")
Design=WaveGuide.drawStraight(750, "-x")
Design=WaveGuide.drawTurn(100, "ll", "-x")
Design=WaveGuide.drawStraight(300, "+x")
Design=WaveGuide.drawTurn(100, "r", "+x")
Design=WaveGuide.drawTermination(TerminationQubitCoupling, "-y", GroundPlaneLayer)


#Creates a qubit with a squid at the end
StripWidth=24
SlotWidth=24
CrossLength=354
Transmon=Qubit.Xmon(0, 0, 0, GroundPlaneLayer)
Transmon.setParameters(StripWidth, SlotWidth, CrossLength)
Transmon.draw()

Transmon.RelSetPoint("-y", 0, 5)
Transmon.drawTermination(TerminationTPatch, "-y", PatchLayer)
Transmon.RelSetPoint("-y", 0, 1)
Transmon.drawTermination(TerminationSQUID, "-y", JJLayer)
Transmon.RelSetPoint("-y", 0, 3)
Transmon.drawTermination(TerminationUPatch, "-y", PatchLayer)


#Connect the qubit to the waveguide
WaveGuide.RelSetPoint(0, -20)
Design=WaveGuide.ConnectObject(Transmon, "-y")

#Add a flux line next to the Qubit 
WaveGuide.SetPoint(Transmon.BottomCoordinate[0], Transmon.BottomCoordinate[1]-5)
Design=WaveGuide.drawTermination(TerminationFluxLine, "+y", GroundPlaneLayer,Reversed=True)
Design=WaveGuide.drawStraight(400, "-y")
Design=WaveGuide.drawTurn(100, "l", "-y")
Design=WaveGuide.drawStraight(400, "+x")
Design=WaveGuide.drawTurn(100, "r", "+x")
Design=WaveGuide.drawTermination(TerminationPad, "-y", GroundPlaneLayer)



WaveGuide.SetPoint(Transmon.RightCoordinate[0]+30, Transmon.RightCoordinate[1])
Design=WaveGuide.drawTermination(TerminationQubitDrive, "-x", GroundPlaneLayer,Reversed=True)
Design=WaveGuide.drawStraight(400, "+x")
Design=WaveGuide.drawTurn(100, "r", "+x")
Design=WaveGuide.drawStraight(400, "-y")
Design=WaveGuide.drawTurn(100, "l", "-y")
Design=WaveGuide.drawTermination(TerminationPad, "+x", GroundPlaneLayer)

ChipCell.add(Design)
lib.write_gds('ExampleQubit.gds')