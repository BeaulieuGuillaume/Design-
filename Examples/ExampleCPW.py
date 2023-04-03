# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 11:22:54 2022

Example to show how to use the CPW elements

@author: beaulieu
"""

import numpy as np
import gdspy
from GDS import CPWGuide as CP

lib = gdspy.GdsLibrary()
gdspy.current_library = lib
ChipCell=lib.new_cell("ChipCell")

#%% Define all of the parameters


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


#Parameters for the opening
StripWidth=16.692
SlotWidth=10
OpeningWidth=StripWidth+2*SlotWidth
OpeningLength=16.657
TerminationOpening={"CPWOpening":[OpeningWidth, OpeningLength]}

#%% Makes the chip design

GroundPlaneLayer=1
StripWidth=16.692
SlotWidth=10

#Fines the CPW class
CPW=CP.CPWGuide(0,0,0,GroundPlaneLayer)
CPW.setParameters(StripWidth, SlotWidth)

#FeedLine
Cell=CPW.drawTermination(TerminationPad, "-x", GroundPlaneLayer,Reversed=True) #Creates a Pad from 0,0
Cell=CPW.drawStraight(5700, "+x") #Draw the feeline
Cell=CPW.drawTermination(TerminationPad, "+x", GroundPlaneLayer) #Draw the end Pad

#QubitFlux Line
CPW.SetPoint(5820,-3500)
Cell=CPW.drawTermination(TerminationPad, "-y", GroundPlaneLayer,Reversed=True)
Cell=CPW.drawTurn(120, "l", "+y")
Cell=CPW.drawStraight(720, "-x")
Cell=CPW.drawTurn(120, "r", "-x")
Cell=CPW.drawStraight(320, "+y")
Cell=CPW.drawTermination(TerminationFluxLine, "+y", GroundPlaneLayer)


#QubitDrive Line
CPW.SetPoint(6700,-2400)
Cell=CPW.drawTermination(TerminationPad, "+x", GroundPlaneLayer,Reversed=True)
Cell=CPW.drawTurn(120, "r", "-x")
Cell=CPW.drawStraight(500, "+y")
Cell=CPW.drawTurn(120, "l", "+y")
Cell=CPW.drawStraight(465, "-x")
Cell=CPW.drawTermination(TerminationQubitDrive, "-x", GroundPlaneLayer)


#QubitResonator Line
CPW.SetPoint(1600,-547)
Cell=CPW.drawTermination(TerminationQubitCoupling, "-y", GroundPlaneLayer,Reversed=True)
Cell=CPW.drawStraight(350, "+y")
Cell=CPW.drawTurn(100, "r", "+y")
Cell=CPW.drawStraight(410, "+x")
Cell=CPW.drawTurn(100, "r", "+x")
Cell=CPW.drawStraight(420, "-y")
Cell=CPW.drawTurn(100, "l", "-y")
Cell=CPW.drawStraight(1060, "+x")
Cell=CPW.drawTurn(100, "rr", "+x")
Cell=CPW.drawStraight(1060, "-x")
Cell=CPW.drawTurn(100, "ll", "-x")
Cell=CPW.drawStraight(1060, "+x")
Cell=CPW.drawTurn(100, "rr", "+x")
Cell=CPW.drawStraight(450, "-x")
Cell=CPW.drawTurn(100, "l", "-x")
Cell=CPW.drawTermination(TerminationOpening, "-y",GroundPlaneLayer)

#Qubit drive Line but from the reference of the line
CPW.SetPoint(4000,-65)
Cell=CPW.drawTurn(100, "l", "-x")
Cell=CPW.drawStraight(350, "-y")
Cell=CPW.drawTermination(TerminationQubitCoupling, "-y",GroundPlaneLayer)

ChipCell.add(Cell)
lib.write_gds('ExampleCPW.gds')
