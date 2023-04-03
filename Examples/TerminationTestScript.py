# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:43:39 2022

Script for testing all of the terminations individually and their attachement to waveguide. 

@author: beaulieu
"""


import numpy as np
import gdspy
from GDS import Termination
from GDS import CPWGuide as CP
#from Termination import CPWGuide,CPWQubitCoupling,CPWPad, UPatch,TPatch,DoubleAngleJunction, CPWOpening, TestPad, CPWQubitDriveLine, CPWFluxLine


lib = gdspy.GdsLibrary()
gdspy.current_library = lib


TerminationCell=lib.new_cell("TerminationCell")
AttachmentCell=lib.new_cell("AttachementCell")


#%% Test of the CPWPad class

#Parameters
Direction="+x"
Layer=1

#Parameters for the Pads
StripWidth=16.692
SlotWidth=10
PadWidth=150.756
OffsetPadEtch=100
PadLength=200
ImpMatchLength=200
TerminationPad={"CPWPad":[PadWidth,OffsetPadEtch,PadLength,ImpMatchLength]}


#Class Test
Pad=Termination.CPWPad(0,0,Direction,Layer)
Pad.setParameters(PadWidth, OffsetPadEtch, PadLength, ImpMatchLength, StripWidth, SlotWidth)
PadCell=lib.new_cell("PadCell")
PadCell.add(Pad.draw())
TerminationCell.add(gdspy.CellReference(PadCell))

#Attachement Test
CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawStraight(550, "+x")
Cell=CPW.drawTermination(TerminationPad, "-x",Layer,Reversed=True)
Cell=CPW.drawStraight(550, "+x")


PadCellAttach=lib.new_cell("PadCellAttach")
PadCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(PadCellAttach))


#%% Test of the CPWOpening Class

#Parameters
Direction="-x"
Layer=1

#Parameters for the opening
StripWidth=16.692
SlotWidth=10

OpeningWidth=SlotWidth*3
OpeningLength=16.657
TerminationOpening={"CPWOpening":[OpeningWidth, OpeningLength]}

#Class Test
Opening=Termination.CPWOpening(10, 10, Direction, Layer)
Opening.setParameters(OpeningWidth, OpeningLength)
OpeningCell=lib.new_cell("OpeningCell")
OpeningCell.add(Opening.draw())
TerminationCell.add(gdspy.CellReference(OpeningCell))


#Attachement Test
CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
CPW.drawTermination(TerminationOpening, Direction,Layer)
CPW.drawStraight(500,Direction)
CPW.drawTermination(TerminationOpening, Direction,Layer)
Cell=CPW.drawStraight(500,Direction)

OpeningCellAttach=lib.new_cell("OpeningCellAttach")
OpeningCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(OpeningCellAttach))


#%% Test of the CPWQubitCoupling

#Parameters
Direction="-y"
Layer=1

#CPW parameters
StripWidth=16.692
SlotWidth=10

#Qubit Coupling Parameters
CentralConductorWidth=100
SideConductorWidth=42
SideLength=144
TerminationQubitCoupling={"CPWQubitCoupling":[CentralConductorWidth,SideConductorWidth,SideLength]}

QubitCoupling=Termination.CPWQubitCoupling(0, 0, Direction, Layer)
QubitCoupling.setParameters(CentralConductorWidth, SideConductorWidth, SideLength, StripWidth, SlotWidth)
QubitCouplingCell=lib.new_cell("QubitCouplingCell")
QubitCouplingCell.add(QubitCoupling.draw())
TerminationCell.add(gdspy.CellReference(QubitCouplingCell))

#Attachement Test
CPW=CP.CPWGuide(10, 10, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
CPW.drawStraight(500,Direction)
CPW.drawTermination(TerminationQubitCoupling, "+y",Layer,Reversed=True)
CPW.drawStraight(500,Direction)
CPW.drawTermination(TerminationQubitCoupling, Direction,Layer)
Cell=CPW.drawStraight(500,Direction)

QubitCouplingCellAttach=lib.new_cell("QubitCouplingCellAttach")
QubitCouplingCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(QubitCouplingCellAttach))


#%% Test of the CPWDriveLine

#Parameters
Direction="+y"
Layer=1

#CPW parameters
InitStripWidth=16.692
InitSlotWidth=10
FinStripWidth=5
FinSlotWidth=3.032
TaperedLength=10
StraightLength=288.484
TerminationQubitDrive={"CPWQubitDriveLine":[FinStripWidth,FinSlotWidth,TaperedLength,StraightLength]}


DriveLine=Termination.CPWQubitDriveLine(0, 0, Direction, Layer)
DriveLine.setParameters(InitStripWidth, InitSlotWidth, FinStripWidth, FinSlotWidth, TaperedLength, StraightLength)
DriveLineCell=lib.new_cell("DriveLineCell")
DriveLineCell.add(DriveLine.draw())
TerminationCell.add(gdspy.CellReference(DriveLineCell))


#Attachement Test
CPW=CP.CPWGuide(10, 10, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawTermination(TerminationQubitDrive, "+y",Layer,Reversed=True)
CPW.drawStraight(500,"-y")
CPW.drawTermination(TerminationQubitDrive, "-y",Layer)
Cell=CPW.drawStraight(500,"-y")

QubitDriveCellAttach=lib.new_cell("QubitDriveCellAttach")
QubitDriveCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(QubitDriveCellAttach))

#%% Test of the CPWFluxLine

#Parameters
Direction="+x"
Layer=1


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

FluxLine=Termination.CPWFluxLine(10, 10, Direction, Layer)
FluxLine.setParameters(InitStripWidth, InitSlotWidth, FinStripWidth, FinSlotWidth, TaperedLength, StraightLength, Gap, OpeningLength, OpeningOffset)
FluxLineCell=lib.new_cell("FluxLineCell")
FluxLineCell.add(FluxLine.draw())
TerminationCell.add(gdspy.CellReference(FluxLineCell))

#Attachement Test
CPW=CP.CPWGuide(10, 10, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
CPW.drawTermination(TerminationFluxLine, "+y",Layer,Reversed=True)
CPW.drawStraight(500,"-y")
Cell=CPW.drawTermination(TerminationFluxLine, "-y",Layer)
FluxLineCellAttach=lib.new_cell("FluxLineCellAttach")
FluxLineCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(FluxLineCellAttach))

#%% Test of the TPatch

#Parameters
Direction="+y"
Layer=1

#Parameters of the TPATCH
TotalWidth=10
PartialHeight=5.62
TopWidth=5
RadiusCorner=0.5
TotalHeight=12.08
TopHeight=1.5
TerminationTPatch={"TPatch":[TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight]}

Patch=Termination.TPatch(0, 0, Direction, Layer)
Patch.setParameters(TotalWidth, PartialHeight, TopWidth, RadiusCorner, TotalHeight, TopHeight)
PatchCell=lib.new_cell("TPatchCell")
PatchCell.add(Patch.draw())
TerminationCell.add(gdspy.CellReference(PatchCell))


CPW=CP.CPWGuide(10, 10, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
CPW.drawTermination(TerminationTPatch, "+y",Layer,Reversed=True)
Cell=CPW.drawStraight(500,"-y")
TPatchCellAttach=lib.new_cell("TPatchCellAttach")
TPatchCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(TPatchCellAttach))

#%% Test of the UPatch


#Parameters
Direction="+x"
Layer=1


#Parameters of the UPatch
SideWidth=4.75
BottomHeight=3
RadiusCorner=0.5
SideHeight=11.66
TotalWidth=15
TerminationUPatch={"UPatch":[SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth]}

Patch=Termination.UPatch(0, 0, Direction, Layer)
Patch.setParameters(SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth)
PatchCell=lib.new_cell("UPatchCell")
PatchCell.add(Patch.draw())
TerminationCell.add(gdspy.CellReference(PatchCell))



CPW=CP.CPWGuide(10, 10, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
CPW.drawTermination(TerminationUPatch, "+y",Layer)
Cell=CPW.drawStraight(500,"+y")
UPatchCellAttach=lib.new_cell("UPatchCellAttach")
UPatchCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(UPatchCellAttach))

#%% Test of the SQUID

#Parameters
Direction=90
Layer=1

#Parameters of the JJ
SmallWidth=0.5
LargeWidth=0.85
RestrictedLength=5
TotalLength=14

LeftJunctionX=6
RightJunctionX=4
DisplacementY=1
TerminationSQUID={"SQUIDDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY]}

JJ=Termination.DoubleAngleJunction(10, 10, Direction, Layer)
JJ.setParameters(SmallWidth, LargeWidth, RestrictedLength, TotalLength)
JunctionCell=lib.new_cell("SquidJunctionCell")
JunctionCell.add(JJ.drawSQUID(LeftJunctionX,RightJunctionX,DisplacementY))
TerminationCell.add(gdspy.CellReference(JunctionCell))



CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawTermination(TerminationSQUID, "-y",Layer,Reversed=True)
Cell=CPW.drawStraight(500,"+y")

SQUIDCellAttach=lib.new_cell("SQUIDCellAttach")
SQUIDCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(SQUIDCellAttach))


#%% Test of the Single Junction

#Parameters
Direction=90
Layer=1

#Parameters of the JJ
SmallWidth=0.5
LargeWidth=0.85
RestrictedLength=5
TotalLength=14

LeftJunctionX=6
DisplacementY=1
TerminationJunction={"JunctionDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY]}

SingleJ=Termination.DoubleAngleJunction(10, 10, Direction, 1)
SingleJ.setParameters(SmallWidth, LargeWidth, RestrictedLength, TotalLength)
SingleJunctionCell=lib.new_cell("SingleJunctionCell")
SingleJunctionCell.add(SingleJ.drawJunction(LeftJunctionX, DisplacementY))
TerminationCell.add(gdspy.CellReference(SingleJunctionCell))



CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawStraight(500,"-y")
Cell=CPW.drawTermination(TerminationJunction, "+y",Layer,Reversed=True)
Cell=CPW.drawStraight(500,"-y")
JunctionCellAttach=lib.new_cell("JunctionAttach")
JunctionCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(JunctionCellAttach))

#%% Test of SQUID with undercut

#Parameters
Direction=90
Layer=1

#Parameters of the JJ
SmallWidth=0.5
LargeWidth=0.85
RestrictedLength=5
TotalLength=14

LeftJunctionX=6
RightJunctionX=4
DisplacementY=1
UndercutLayer=2
TerminationJunctionUnderCut={"SQUIDDoubleAngleJunctionUnderCut":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY,UndercutLayer]}



SQUIDUnderCut=Termination.DoubleAngleJunction(10, 10, Direction, 1)
SQUIDUnderCut.setParameters(SmallWidth, LargeWidth, RestrictedLength, TotalLength)
SQUIDUnderCutCell=lib.new_cell("SQUIDUnderCut")
SQUIDUnderCutCell.add(SQUIDUnderCut.drawSQUIDUnderCut(LeftJunctionX,RightJunctionX,DisplacementY,UndercutLayer))
TerminationCell.add(gdspy.CellReference(SQUIDUnderCutCell))

CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawTermination(TerminationJunctionUnderCut, "+y",Layer,Reversed=True)
Cell=CPW.drawStraight(500,"-y")
SQUIDUnderCutCellAttach=lib.new_cell("SQUIDUnderCutAttach")
SQUIDUnderCutCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(SQUIDUnderCutCellAttach))

#%% Test for the TestPad

#Parameters
Direction="+x"
Layer=1

Height=390
Width=192
ConstrictionWidth=30
ConstrictionHeight=22.8
TaperedWidth=50
SlotWidth=10

TerminationTestPad={"TestPad":[Height,Width,ConstrictionWidth,ConstrictionHeight,TaperedWidth]}

Pad=Termination.TestPad(0, 0, Direction, 1)
Pad.setParameters(Height, Width, ConstrictionWidth, ConstrictionHeight, TaperedWidth, SlotWidth)
TestPadCell=lib.new_cell("TestPadCell")
TestPadCell.add(Pad.draw())
TerminationCell.add(gdspy.CellReference(TestPadCell))


CPW=CP.CPWGuide(0, 0, 0, Layer)
CPW.setParameters(StripWidth,SlotWidth)
Cell=CPW.drawTermination(TerminationTestPad, "-x",Layer,Reversed=True)
Cell=CPW.drawStraight(500, "+x")
TestPadCellAttach=lib.new_cell("TestPadAttach")
TestPadCellAttach.add(Cell)
AttachmentCell.add(gdspy.CellReference(TestPadCellAttach))




lib.write_gds('TerminationTest.gds')




