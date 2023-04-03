# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 19:31:50 2022

@author: beaulieu


#Want to create a method that makes an array
"""

import gdspy
import numpy as np
import math
from GDS import Utility

class AlignmentLines:
    """Class made to draw the alignment lines on the wafer"""
    
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("ALIGNMENT_LINE")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.layer=layer
       
        
    def setParameters(self, AlignmentLineWidth, AlignmentLineOffset,ChipSizeX,ChipSizeY):
        """
        AlignementLineWidth : Width of the alignement marks
        AlignmentLineOffset : define the space between the alignment line and the chip
        ChipSizeX : size of a single chip in X
        ChipSizeY : size of a single chip in Y 
        """
         
        self.AlignmentLineWidth=AlignmentLineWidth
        self.AlignmentLineOffset=AlignmentLineOffset
        self.AlignmentLineLengthX=ChipSizeX-2*AlignmentLineOffset
        self.AlignmentLineLengthY=ChipSizeY-2*AlignmentLineOffset
       
   
       
        
    def drawx(self):

        """
        Draw an alignment line in the x direction 
        """
        
        AlignmentLine=gdspy.Path(self.AlignmentLineWidth,(0,0))
        AlignmentLine.segment(self.AlignmentLineLengthX,'+x',layer=self.layer)
        
        self.cell.add(AlignmentLine)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    def drawy(self):
        
        
        """
        Draw an alignment line in the y direction 
        """
        
        AlignmentLine=gdspy.Path(self.AlignmentLineWidth,(0,0))
        AlignmentLine.segment(self.AlignmentLineLengthY,'+y',layer=self.layer)
        
        self.cell.add(AlignmentLine)
        
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        
    
    
    def drawArray(self,NbRow,NbColumn,ChipSizeX,ChipSizeY):
    
        """
        Draw alignment line over the wafer (Method to be improved to use the previous methods)
        """
            
        for i in range(NbColumn):
            for j in range(NbRow+1):
              AlignmentLine=gdspy.Path(self.AlignmentLineWidth,(i*ChipSizeX+self.AlignmentLineOffset,j*ChipSizeY))
              AlignmentLine.segment(self.AlignmentLineLengthX,'+x',layer=self.layer)
              self.cell.add(AlignmentLine)
              
              
        for i in range (NbColumn+1):
            for j in range (NbRow):
                AlignmentLine=gdspy.Path(self.AlignmentLineWidth,(i*ChipSizeX,j*ChipSizeY+self.AlignmentLineOffset))
                AlignmentLine.segment(self.AlignmentLineLengthY,'+y',layer=self.layer)
                self.cell.add(AlignmentLine)
                
                
          
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
                
    
    
    
    
    
    
    
class AlignmentMarkers :
    
    """Class made to draw the alignment marks on the wafer"""
    
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("ALIGNMENT_MARKER")
        MarkerCell=lib.new_cell("MARKER")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.MarkerCell=MarkerCell
        self.layer=layer
        
    def setParameters(self, MarkerSize,MarkerArraySize,ArraySpacing):
        """
        MarkerSize : Size of each square marker
        MarkerArraySize : Define the size of the array (odd number giving the number of squares)
        ArraySpacing : spacing between the markers inside the array 
        """
        self.MarkerSize=MarkerSize
        self.MarkerArraySize=MarkerArraySize
        self.ArraySpacing=ArraySpacing
        
        
    
    def draw(self):
        
        """
        Method to draw a single array of the square markers  
        """
        
        SingleMarker = gdspy.Rectangle((-self.MarkerSize, -self.MarkerSize), (self.MarkerSize, self.MarkerSize),layer=self.layer)
        self.MarkerCell.add(SingleMarker)
        
        self.cell.add( gdspy.CellArray(self.MarkerCell, self.MarkerArraySize, self.MarkerArraySize, (self.ArraySpacing, self.ArraySpacing), origin=(-math.floor(self.MarkerArraySize/2)*self.ArraySpacing,-math.floor(self.MarkerArraySize/2)*self.ArraySpacing)))        
             
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    def drawArray(self,NbRow,NbColumn,ChipSizeX,ChipSizeY):
        
        """
        Method to draw the array over the entire wafer 
        """
        
        
        SingleMarker = gdspy.Rectangle((-self.MarkerSize, -self.MarkerSize), (self.MarkerSize, self.MarkerSize),layer=self.layer)
        self.MarkerCell.add(SingleMarker)
        
        for i in range(NbRow+1) :
            
            for j in range(NbColumn+1) :
                
                self.cell.add( gdspy.CellArray(self.MarkerCell, self.MarkerArraySize, self.MarkerArraySize, (self.ArraySpacing, self.ArraySpacing), origin=(-math.floor(self.MarkerArraySize/2)*self.ArraySpacing+j*ChipSizeX,-math.floor(self.MarkerArraySize/2)*self.ArraySpacing+i*ChipSizeY)))    
                
        
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    
    
    
class AlignmentGrid:
    """
    Class that makes the alignment grid used for e-beam exposure. It consists of markers that are incrementally spaced from the center. 
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("ALIGNMENT_GRID")
        MarkerCell=lib.new_cell("MARKER")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.MarkerCell=MarkerCell
        self.layer=layer
        
    def setParameters(self, MarkerSize,MarkerDistance,OffSet,ArraySize):
        """
        MarkerSize : Size of each square marker
        MarkerDistance: Distance from the center marker
        Offset : added offset to each new marker 
        ArraySize : size of the array (i.e 5 makes a 5 by 5 array)
        """
        self.MarkerSize=MarkerSize
        self.MarkerDistance=MarkerDistance
        self.Offset=OffSet
        self.ArraySize= ArraySize
        
        
    def draw(self):
        
        """
        Method to draw the grid
        """
        SingleMarker=gdspy.Rectangle((-self.MarkerSize/2,-self.MarkerSize/2),(self.MarkerSize/2,self.MarkerSize/2),layer=self.layer) 
        self.MarkerCell.add(SingleMarker)
        
        
        
        #Creation of an array containing all the spacing of the squares in the + x direction
        Spacing=np.full((1,int((self.ArraySize-1)/2)),self.MarkerSize+self.MarkerDistance)+np.arange(start=0,stop=(self.ArraySize-1)/2)*self.Offset
        PositionX=np.cumsum(Spacing)
        
        
        #Creation o the array containing all the spacing
        Position=np.concatenate((-1*np.flip(PositionX),np.array([0]),PositionX))
        
        for j in range(self.ArraySize):
            
            for i in range(self.ArraySize):
                
                origin=(Position[i],Position[j])
                ref=gdspy.CellReference(self.MarkerCell,origin=origin)
                
                self.cell.add(ref)
            
        
        
             
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
   


         

class AlignmentCross:
    """
    Class that makes an alignment cross to observe if there is a drift during the MLA exposure 
    """
    
    def __init__(self, coord_x, coord_y, rotation,layerSquare, layerCross):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("ALIGNMENT_GRID")
        MarkerCell=lib.new_cell("MARKER")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.MarkerCell=MarkerCell
        self.layerSquare=layerSquare
        self.layerCross= layerCross
        
        
    def setParameters(self, SquareSize, Spacing, CrossWidth):
        """
        SquareSize : Size of each square marker
        Spacing: Spacing between the initial markers 
        """
        
        self.SquareSize=SquareSize
        self.Spacing=Spacing
        self.CrossWidth=CrossWidth
        
        
    def draw(self):  
        """
        Method to draw the alignment cross
        """   
    
        
        #Draw four rectangles 
        rectBottomLeft=gdspy.Rectangle((-self.Spacing/2,-self.Spacing/2),(-self.Spacing/2-self.SquareSize,-self.Spacing/2-self.SquareSize),layer= self.layerSquare)
        rectBottomRight=gdspy.Rectangle((self.Spacing/2,-self.Spacing/2),(self.Spacing/2+self.SquareSize,-self.Spacing/2-self.SquareSize),layer= self.layerSquare)
        rectTopRight=gdspy.Rectangle((self.Spacing/2,self.Spacing/2),(self.Spacing/2+self.SquareSize,self.Spacing/2+self.SquareSize),layer= self.layerSquare)
        rectTopLeft=gdspy.Rectangle((-self.Spacing/2,self.Spacing/2),(-self.Spacing/2-self.SquareSize,self.Spacing/2+self.SquareSize),layer= self.layerSquare)
        
        #Draw the center cross 
        CrossH=gdspy.Rectangle( (-self.Spacing/2-self.SquareSize,self.CrossWidth/2), (self.Spacing/2+self.SquareSize,-self.CrossWidth/2),layer=self.layerCross)
        CrossV=gdspy.Rectangle( (-self.CrossWidth/2,-self.Spacing/2-self.SquareSize),(self.CrossWidth/2,self.Spacing/2+self.SquareSize), layer=self.layerCross )
        
      
        #Add all of the elements to the MarkerCell
        self.MarkerCell.add([rectBottomLeft,rectBottomRight,rectTopRight,rectTopLeft,CrossH, CrossV])
        
        #Creates a 4x4 array 
        self.cell.add(gdspy.CellArray(self.MarkerCell,2,2,(100+self.Spacing+2*self.SquareSize,100+self.Spacing+2*self.SquareSize),origin=(-100/2-self.Spacing/2-self.SquareSize,-100/2-self.Spacing/2-self.SquareSize) ))
        
       
        
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    
class ChipNumber :
    """
    Class that places a number on each chip 
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CHIPNUMBER")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.layer=layer
        
    def setParameters(self, FontSize):
        """
       FontSize of the Number
        """
        self.FontSize=FontSize
        
    def draw(self,NbRow,NbColumn,ChipSizeX,ChipSizeY, XOffset, YOffset):
        
        """
        Method to draw the numbers over the entire wafer
        """
        
        
        UpdatedFontSize=self.FontSize*1.2857106122553934
        VerticalOffset=0.2855*self.FontSize
        Number=1
        
        for i in range(NbRow) :
            
            for j in range(NbColumn) :
                
               
                
                self.cell.add( gdspy.Text(str(Number)+"-",UpdatedFontSize,position=(j*ChipSizeX+XOffset,i*ChipSizeY-VerticalOffset+YOffset),layer=self.layer))    
                Number+=1
        
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
class ChipLabel :
    """
    Class that places an added Label on each Chip
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CHIPLABEL")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.layer=layer
        
    def setParameters(self, FontSize):
        """
       FontSize of the Number
        """
        self.FontSize=FontSize
        
    def draw(self,NbRow,NbColumn,ChipSizeX,ChipSizeY, XOffset, YOffset):
        
        """
        Method to draw the numbers over the entire wafer
        """
        
        
        UpdatedFontSize=self.FontSize*1.2857106122553934
        VerticalOffset=0.2855*self.FontSize
        
        Label="EPFL"
        
        for i in range(NbRow) :
            
            for j in range(NbColumn) :
                
                
                self.cell.add( gdspy.Text(Label,UpdatedFontSize,position=(j*ChipSizeX+XOffset,i*ChipSizeY-VerticalOffset+YOffset),layer=self.layer))    
                
        
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
     
    