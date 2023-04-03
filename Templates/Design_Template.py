# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 18:43:23 2022

@author: beaulieu
"""

from GDS import Wafer
from GDS import Alignment as Align
from GDS import Utility
import gdspy

lib = gdspy.GdsLibrary()
gdspy.current_library = lib


#%% Creates the Wafer and alignment marks

#Set the layers 
WaferLayer=0
AlignmentLayer=3
GroundPlaneLayer=4


### Creates the outer 4" wafer cell at 00
WaferCell = lib.new_cell("WAFER") 
Wafer=Wafer.Wafer4(0,0,0,WaferLayer) 
WaferCell.add(Wafer.drawWafer4())

### Creates all of the alignment marks 

AlignmentCell=lib.new_cell("ALIGNMENT")  #Cell containing all the alignment object


#Dimensions of each chip
ChipSizeX=7000 # Size of chip in x
ChipSizeY=4000 # Size of chip in y
NbRow=15 # Number of rows (chip)
NbColumn=9 # Number of Columns (chip)


#Create the alignment grid 
AlignmentGridCell=lib.new_cell("ALIGNMENTGRID")

# Parameters for the alignment grids 
MarkerSize=10
MarkerDistance=65
OffSet=1
ArraySize=49

#creates the alignment grid
AlignmentGrid=Align.AlignmentGrid(0,0,0,AlignmentLayer)
AlignmentGrid.setParameters(MarkerSize, MarkerDistance, OffSet, ArraySize)
AlignmentGridCell.add(AlignmentGrid.draw())

#Repeat the alignment grid at different positions and add it to the alignmentcell
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(34500,16500))) 
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(34500,-16500)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(34500,12000)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(34500,-12000)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(-34500,16500)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(-34500,-16500)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(-34500,12000)))
AlignmentCell.add(gdspy.CellReference(AlignmentGridCell,origin=(-34500,-12000)))



#Create the alignment lines
AlignmentLineCell=lib.new_cell("ALIGNMENTLINE")

#Parameters for the alignment lines 
AlignmentLineWidth=10 # Widht of the alignment lines
AlignmentLineOffset=750 # Space between corner of chip and alignment marks

#create the alignement lines
AlignmentLines=Align.AlignmentLines(0,0,0,AlignmentLayer)
AlignmentLines.setParameters(AlignmentLineWidth, AlignmentLineOffset, ChipSizeX, ChipSizeY)
AlignmentLineCell.add(AlignmentLines.drawArray(NbRow,NbColumn,ChipSizeX,ChipSizeY))
AlignmentCell.add(gdspy.CellReference(AlignmentLineCell,origin=(-ChipSizeX*NbColumn/2,-ChipSizeY*NbRow/2))) #add the lines to the alignmentcell




#**** This is commented since not present in the mask

# AlignmentCrossCell=lib.new_cell("ALIGNMENTCROSS")

# #Parameters for the alignment cross
# SquareSize=90
# Spacing=20
# CrossWidth=10
# OffSet=450 #Spacing between the alignment grid and the marker

# #Creates one alignment cross
# AlingmentOffset=AlignmentCross(0, 0, 0, AlignmentLayer,GroundPlaneLayer)
# AlingmentOffset.setParameters(SquareSize, Spacing, CrossWidth)
# AlignmentCrossCell.add(AlingmentOffset.draw())

# #Creates an array around the wafer
# AlignmentCell.add(gdspy.CellArray(AlignmentCrossCell, NbColumn, 2, (ChipSizeX,ChipSizeY*NbRow+OffSet*2),origin=(-(NbColumn-1)*ChipSizeX/2,-ChipSizeY*NbRow/2-OffSet)))
# AlignmentCell.add(gdspy.CellArray(AlignmentCrossCell, 2, NbRow, (ChipSizeX*NbColumn+OffSet*2,ChipSizeY),origin=(-ChipSizeX*NbColumn/2-OffSet,-(NbRow-1)*ChipSizeY/2)))





#Create the alignment marks
AlignmentMarkCell=lib.new_cell("ALIGNMENTMARKS")

#Parameters for the array 
MarkerSize=10 # Size of the marker
MarkerArraySize=5 # Size of the array of markers (5x5)
ArraySpacing=250 # Spacing between the markers in the Array

AlignmentMarkers=Align.AlignmentMarkers(0,0,0,AlignmentLayer)
AlignmentMarkers.setParameters(MarkerSize, MarkerArraySize, ArraySpacing)
AlignmentMarkCell.add(AlignmentMarkers.drawArray(NbRow,NbColumn,ChipSizeX,ChipSizeY))
AlignmentCell.add(gdspy.CellReference(AlignmentMarkCell,origin=(-ChipSizeX*NbColumn/2,-ChipSizeY*NbRow/2)))

#Add the alignment cell to the wafer
WaferCell.add(gdspy.CellReference(AlignmentCell,origin=(0,0)))



#%% Fill the Wafer with chips 

#Creates and empty list to position all the cells over the wafer
ChipList=[[None for i in range(NbColumn)] for j in range(NbRow)]


#Example of a simple cell containing a rectangle 
TestCell=lib.new_cell("TEST")
Rectangle=gdspy.Rectangle((-1000,-1000),(1000,1000))
TestCell.add(Rectangle)

ChipList[3][1]=TestCell
ChipList[2][2]=TestCell
ChipList[14][8]=TestCell


WaferCell=Utility.PopulateWafer(ChipList, WaferCell,ChipSizeX,ChipSizeY)



lib.write_gds('DesignTemplate.gds')



