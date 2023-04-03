# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:16:16 2022

This script regroups all of the class that can be simply defined by two attach point (red point : starting point and blue point : end point)


@author: beaulieu
"""
import gdspy
from GDS import Utility
import numpy as np

    
    
class CPWPad:
    """
    Class for creating bonding pads connecting to the CPW waveguide
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CPWPAD")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,PadWidth,OffsetPadEtch,PadLength,ImpMatchLength,StripWidth,SlotWidth ):
        """
        PadWidth : Width of bonding Pad
        OffsetPadEtch : Width of the spcaing between the bonding pad and the groumd
        PadLength : Length of the rectangular region of the pad
        ImpMatchLenght : Length of the tapper region connecting the rectangular part to the waveguide
        StripWidth : Width of the conducting region of the CPW
        SlotWidth : Width of the spcaing between the conducting channel and the groumd
        """
        self.PadWidth=PadWidth
        self.OffsetPadEtch=OffsetPadEtch
        self.PadLength=PadLength
        self.ImpMatchLength=ImpMatchLength
        self.StripWidth=StripWidth
        self.SlotWidth=SlotWidth
           
           
    def draw(self):
        """
        Method for drawing the Pad
        """
        #Creates the inner and outer bound impedance match
        ImpMatch = gdspy.Path(self.PadWidth, initial_point = (-self.ImpMatchLength, 0))
        ImpMatch.segment(self.ImpMatchLength,direction="+x",final_width=self.StripWidth,layer=self.layer)
        
        
        ImpMatchEtch = gdspy.Path(self.PadWidth+self.OffsetPadEtch*2, initial_point = (-self.ImpMatchLength, 0))
        ImpMatchEtch.segment(self.ImpMatchLength,direction="+x",final_width=self.StripWidth+self.SlotWidth*2,layer=self.layer)
        
        
        #Creates the inner and outer bound rectangle
        Pad=gdspy.Rectangle((-self.ImpMatchLength-self.PadLength,-self.PadWidth/2)   , (-self.ImpMatchLength,self.PadWidth/2),layer=self.layer )
        
        PadEtch=gdspy.Rectangle((-self.ImpMatchLength-self.PadLength-self.OffsetPadEtch,-self.PadWidth/2-self.OffsetPadEtch),(-self.ImpMatchLength,self.PadWidth/2+self.OffsetPadEtch),layer=self.layer)
        
        #Makes the boolean operation between the outer and inner
        DifferenceImpMatch=gdspy.boolean(ImpMatchEtch, ImpMatch, "not",layer=self.layer)
        DifferencePad=gdspy.boolean(PadEtch, Pad, "not",layer=self.layer)
        
        
        self.cell.add([DifferenceImpMatch,DifferencePad])
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    

    
class CPWOpening:
    """
    Class for creating an opening in the ground plane
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CPWOPENING")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,OpeningWidth, OpeningLength ):
        """
        OpeningWidth : Width of the opening
        OpeningLength: Length of the opening 
        """
        self.OpeningWidth=OpeningWidth
        self.OpeningLength=OpeningLength
           
           
    def draw(self):
        """
        Method for drawing opening
        """
        
        #Draw the rectangle 
        cut=gdspy.Rectangle((0,-self.OpeningWidth/2), (self.OpeningLength,self.OpeningWidth/2),layer=self.layer)
        
        self.cell.add(cut)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)


    
    
    
    
class CPWQubitCoupling:
    """
    Class for creating a coupling termination to a Qubit"""
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CPWQUBITCOUPLING")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
        
    def setParameters(self,CentralConductorWidth,SideConductorWidth,SideLength,StripWidth,SlotWidth):
        """
        CentralConductorWidth : Width of the conductor between the two side rectangles
        SideConductor Width of the side conductor elements
        SideLength : Length of the side conductors
        StripWidth : Width of the strip line to which the qubitcoupling element is linked
        SlotWidth : Width of the slots to which the qubitcoupling element is linked
        """
        self.CentralConductorWidth=CentralConductorWidth
        self.SideConductorWidth=SideConductorWidth
        self.SideLength=SideLength
        self.StripWidth=StripWidth
        self.SlotWidth=SlotWidth
        
        
    def draw(self):
        """
        Method for drawing the Qubit Coupling element 
        """
        
        
        OffsetSideRectangle=self.CentralConductorWidth/2
        
        #Creates the two side rectangle and an offset so make the difference 
        OuterRectangleSideLeft=gdspy.Rectangle((-2*self.SlotWidth-self.SideConductorWidth-OffsetSideRectangle,-self.SideLength-2*self.SlotWidth),(-OffsetSideRectangle,0))
        InnerRectangleSideLeft=gdspy.offset(OuterRectangleSideLeft, -self.SlotWidth)
        
        OuterRectangleSideRight=gdspy.Rectangle((2*self.SlotWidth+self.SideConductorWidth+OffsetSideRectangle,-self.SideLength-2*self.SlotWidth),(OffsetSideRectangle,0))
        InnerRectangleSideRight=gdspy.offset(OuterRectangleSideRight, -self.SlotWidth)
        
        
        #Creates the center rectangle and an offset of it
        OuterRectangleCenter=gdspy.Rectangle((-OffsetSideRectangle,0),(OffsetSideRectangle,-self.SlotWidth*2-self.StripWidth))
        InnerRectangleCenter=gdspy.Rectangle((-OffsetSideRectangle-self.SlotWidth,-self.SlotWidth),(OffsetSideRectangle+self.SlotWidth,-self.SlotWidth-self.StripWidth))
        
        #Takes the difference between the center and outer element
        DifferenceRectangleSideLeft=gdspy.boolean(OuterRectangleSideLeft, InnerRectangleSideLeft, "not",layer=self.layer)
        DifferenceRectangleSideRight=gdspy.boolean(OuterRectangleSideRight, InnerRectangleSideRight, "not",layer=self.layer)
        DifferenceRectangleCenter=gdspy.boolean(OuterRectangleCenter,  InnerRectangleCenter, "not",layer=self.layer)
        
        
        #Removes additional small rectangle to correctly open the shape 
        RectangleConnectSideLeft=gdspy.Rectangle((-OffsetSideRectangle-self.SlotWidth,-self.SlotWidth),(-OffsetSideRectangle,-self.SlotWidth-self.StripWidth))
        RectangleConnectSideRight=gdspy.Rectangle((OffsetSideRectangle+self.SlotWidth,-self.SlotWidth),(OffsetSideRectangle,-self.SlotWidth-self.StripWidth))
        RectangleConnectCenter=gdspy.Rectangle((-self.StripWidth/2,-self.SlotWidth),(self.StripWidth/2,0))
        
        DifferenceRectangleSideLeft=gdspy.boolean(DifferenceRectangleSideLeft,  RectangleConnectSideLeft, "not",layer=self.layer)
        DifferenceRectangleSideRight=gdspy.boolean(  DifferenceRectangleSideRight, RectangleConnectSideRight, "not",layer=self.layer)
        DifferenceRectangleCenter=gdspy.boolean(DifferenceRectangleCenter,  RectangleConnectCenter, "not",layer=self.layer)
        
        
        self.cell.add([DifferenceRectangleSideLeft,DifferenceRectangleSideRight,DifferenceRectangleCenter])
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        
 
        
    
class CPWQubitDriveLine :
    """Class for creating a driving line for a Qubit"""
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("QUBITDRIVE")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,InitStripWidth, InitSlotWidth, FinStripWidth, FinSlotWidth, TaperedLength, StraightLength ):
        """
        InitStripWidth : Initial width of the CPW
        InitSlotWidth: InitialWidth of the slots around the CPW
        FinStripWidth : Final strip width of the CPW
        FinSlotWidth : Final slot width of the CPW
        TaperedLength : length of the tapered region
        StraightLength: Length of the straight region
        """
        self.InitStripWidth=InitStripWidth
        self.InitSlotWidth=InitSlotWidth
        self.FinStripWidth=FinStripWidth
        self. FinSlotWidth= FinSlotWidth
        self.TaperedLength=TaperedLength
        self.StraightLength=StraightLength
    
        
    def draw(self):
        """
        Method for drawing the drive line
        """
        #Creates the inner and outer bound impedance match
        ImpMatchOuter = gdspy.Path(self.InitStripWidth+2*self.InitSlotWidth, initial_point = (0, 0))
        ImpMatchOuter.segment(self.TaperedLength,direction="+x",final_width=self.FinStripWidth+2*self.FinSlotWidth,layer=self.layer)   
        
        ImpMatchInner = gdspy.Path(self.InitStripWidth, initial_point = (0, 0))
        ImpMatchInner.segment(self.TaperedLength,direction="+x",final_width=self.FinStripWidth,layer=self.layer)  
        
        DifferenceImpMatch=gdspy.boolean(ImpMatchOuter, ImpMatchInner, "not",layer=self.layer)
        
        #Created the drive straight section of the drive line
        DriveLine = gdspy.Path(self.FinSlotWidth, initial_point = (self.TaperedLength, 0), number_of_paths=2,distance=self.FinStripWidth+self.FinSlotWidth)
        DriveLine.segment(self.StraightLength,direction="+x",layer=self.layer)     
        
        #Closes the drive line 
        EndOpening=gdspy.Rectangle((self.TaperedLength+self.StraightLength,-self.FinStripWidth/2-self.FinSlotWidth),(self.FinSlotWidth+self.TaperedLength+self.StraightLength,self.FinStripWidth/2+self.FinSlotWidth),layer=self.layer)
        
        self.cell.add([DifferenceImpMatch, DriveLine, EndOpening])
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
                
          

    
class CPWFluxLine :
    """Class for creating a Flux line """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("FLUXLINE")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,InitStripWidth, InitSlotWidth, FinStripWidth, FinSlotWidth, TaperedLength, StraightLength, Gap, OpeningLength, OpeningOffset):
        """
        InitStripWidth : Initial width of the CPW
        InitSlotWidth: InitialWidth of the slots around the CPW
        FinStripWidth : Final strip width of the CPW
        FinSlotWidth : Final slot width of the CPW
        TaperedLength : length of the tapered region
        StraightLength: Length of the straight region
        Gap : connexion at the end of the flux line for current pass
        OpeningLength : length of the opening at the end of the flux line
        OpeningOffset : How much the opening is offset from the line 
        """
        self.InitStripWidth=InitStripWidth
        self.InitSlotWidth=InitSlotWidth
        self.FinStripWidth=FinStripWidth
        self. FinSlotWidth= FinSlotWidth
        self.TaperedLength=TaperedLength
        self.StraightLength=StraightLength
        self.Gap=Gap
        self.OpeningLength=OpeningLength
        self.OpeningOffset=OpeningOffset
    
    
    def draw(self):
        """
        Method for drawing the drive line
        """
        
        #Creates the inner and outer bound impedance match
        ImpMatchOuter = gdspy.Path(self.InitStripWidth+2*self.InitSlotWidth, initial_point = (0, 0))
        ImpMatchOuter.segment(self.TaperedLength,direction="+x",final_width=self.FinStripWidth+2*self.FinSlotWidth,layer=self.layer)   
        
        ImpMatchInner = gdspy.Path(self.InitStripWidth, initial_point = (0, 0))
        ImpMatchInner.segment(self.TaperedLength,direction="+x",final_width=self.FinStripWidth,layer=self.layer)  
        
        DifferenceImpMatch=gdspy.boolean(ImpMatchOuter, ImpMatchInner, "not",layer=self.layer)
        
        #Created the drive straight section of the drive line
        FluxLine = gdspy.Path(self.FinSlotWidth, initial_point = (self.TaperedLength, 0), number_of_paths=2,distance=self.FinStripWidth+self.FinSlotWidth)
        FluxLine.segment(self.StraightLength,direction="+x",layer=self.layer)     
        
        #Closes the drive line 
        GapRectangle=gdspy.Rectangle((self.TaperedLength+self.StraightLength-self.Gap,self.FinStripWidth/2), (self.TaperedLength+self.StraightLength,self.FinStripWidth/2+self.FinSlotWidth))
        FluxLineWithGap=gdspy.boolean(FluxLine,GapRectangle, "not",layer=self.layer)
        
        
        EndOpening=gdspy.Rectangle((self.TaperedLength+self.StraightLength,-self.FinStripWidth/2-self.FinSlotWidth-self.OpeningOffset),(self.FinSlotWidth+self.TaperedLength+self.StraightLength,-self.FinStripWidth/2-self.FinSlotWidth-self.OpeningOffset+self.OpeningLength),layer=self.layer)
        
        self.cell.add([DifferenceImpMatch,FluxLineWithGap,EndOpening])
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)





class TPatch:
        """
        Class for creating a T shape Patch termination 
        """
        
        def __init__(self, coord_x, coord_y, rotation,layer):
            
            lib = gdspy.GdsLibrary()
            gdspy.current_library = lib
            
            cell = lib.new_cell("TPATCH")
            
            
            
            self.coord_x = coord_x
            self.coord_y = coord_y
            self.rotation = rotation
            self.layer=layer
            self.cell = cell
            self.lib = lib
        
        def setParameters(self,TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight):
            """
            TotalWidth : 
            PartialHeight: 
            TopWidth : 
            RadiusCorner : 
            TotalHeight  : 
            TopHeight
            """
            
            self.TotalWidth=TotalWidth
            self.PartialHeight=PartialHeight
            self.TopWidth= TopWidth
            self.RadiusCorner=RadiusCorner
            self.TotalHeight=TotalHeight   
            self.TopHeight=TopHeight
        
        def draw(self):
            
            curve = gdspy.Curve(0, 0).L(self.TotalWidth,0,self.TotalWidth,self.PartialHeight, self.TotalWidth-(self.TotalWidth-self.TopWidth)/2, self.TotalHeight-self.TopHeight,self.TotalWidth-(self.TotalWidth-self.TopWidth)/2,self.TotalHeight-self.RadiusCorner).arc(self.RadiusCorner, 0, np.pi/2)
            curve.L((self.TotalWidth-self.TopWidth)/2+self.RadiusCorner,self.TotalHeight).arc(self.RadiusCorner,np.pi/2,np.pi).L((self.TotalWidth-self.TopWidth)/2,self.TotalHeight-self.TopHeight,0,self.PartialHeight)
            p1 = gdspy.Polygon(curve.get_points(),layer=self.layer)
            
            p1.translate(-self.TotalWidth/2, 0)
            p1.rotate(-np.pi/2,(0,0))
            
            self.cell.add(p1)
            
            return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        





class UPatch:
    """
    Class for creating a U shape Patch termination """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("UPATCH")
        
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
        
    def setParameters(self,SideWidth,BottomHeight,RadiusCorner,SideHeight,TotalWidth):
        """
        SideWidth : Width of the side arms of the U
        BottomHeight: Height of the bottom part of the U 
        SideHeight : Height of the side arms of the U 
        TotalWidth : Total width of the bottom
        RadiusCorner : Radius of the corner (typically 0.5)
        """
        self.SideWidth=SideWidth
        self.BottomHeight=BottomHeight
        self.RadiusCorner=RadiusCorner
        self.SideHeight=SideHeight
        self.TotalWidth=TotalWidth    
    
    def draw(self):
        """
        Method for drawing the U patch 
        """
        
        #Use the polygon tool to draw the shape 
        curve = gdspy.Curve(0, 0).L(self.TotalWidth, 0,self.TotalWidth,self.SideHeight-self.RadiusCorner).arc(self.RadiusCorner, 0, np.pi/2).L( self.TotalWidth- self.SideWidth+self.RadiusCorner,  self.SideHeight)
        curve.arc(self.RadiusCorner,np.pi/2,np.pi).L( self.TotalWidth- self.SideWidth,self.BottomHeight+self.RadiusCorner).arc(self.RadiusCorner, 0, -np.pi/2).L( self.SideWidth+self.RadiusCorner,self.BottomHeight)
        curve.arc(self.RadiusCorner, -np.pi/2, -np.pi).L(self.SideWidth, self.SideHeight-self.RadiusCorner).arc(self.RadiusCorner,0,np.pi/2).L(self.RadiusCorner, self.SideHeight).arc(self.RadiusCorner, np.pi/2, np.pi)
        p1 = gdspy.Polygon(curve.get_points(),self.layer)
        
        #Translate the polygon to set the zeroa
        p1.translate(-self.TotalWidth/2, -self.SideHeight)
     
        self.cell.add(p1)
        
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    



        
class DoubleAngleJunction:
      """
      Class for creating a double angle evaporation of JJ """
      
      def __init__(self, coord_x, coord_y, rotation,layer):
         
          
          lib = gdspy.GdsLibrary()
          gdspy.current_library = lib
          
          VerticalCell = lib.new_cell("VERTICALJUNCTION")
          HorizontallCell = lib.new_cell("HORIZONTALJUNCTION")
          DoubleCell=lib.new_cell("DOUBLEANGLEJUNCTION")
          cell=lib.new_cell("DOUBLEANGLE")
          UnderCutCell=lib.new_cell("UNDERCUTCELL")
          
          
          
          self.coord_x = coord_x
          self.coord_y = coord_y
          self.rotation = rotation
          self.layer=layer
          self.VerticalCell = VerticalCell
          self.HorizontalCell=HorizontallCell
          self.DoubleCell=DoubleCell
          self.UnderCutCell=UnderCutCell
          self.cell=cell
          self.lib = lib
 
      def setParameters(self,SmallWidth ,LargeWidth,RestrictedLength, TotalLength):
            """
            SmallWidth : Width of the Center of the junction
            LargeWidth: Width of the edge of the junctions
            RestrictedLength : Length of the central section
            TotalLength : Total Length 
            """
        
            
            self.SmallWidth=SmallWidth #Smallest width of the junction
            self.LargeWidth=LargeWidth  #Larger width of the junction
            self.RestrictedLength=RestrictedLength #Length of the smaller region of the junction
            self.TotalLength=TotalLength #Total length of the junction
                
            
      def drawHorizontalJunction(self): 
            
            """
            Class drawing an Horizontal junction """
          
            curve = gdspy.Curve(0, -self.SmallWidth/2).L(self.RestrictedLength/2, -self.SmallWidth/2, self.RestrictedLength/2+0.5,-self.LargeWidth/2, self.TotalLength/2,-self.LargeWidth/2,self.TotalLength/2,self.LargeWidth/2)
            curve.L(self.RestrictedLength/2+0.5,self.LargeWidth/2,self.RestrictedLength/2,self.SmallWidth/2,-self.RestrictedLength/2,self.SmallWidth/2, -self.RestrictedLength/2-0.5,self.LargeWidth/2, -self.TotalLength/2, self.LargeWidth/2,-self.TotalLength/2, -self.LargeWidth/2 )
            curve.L(-self.RestrictedLength/2-0.5,-self.LargeWidth/2, -self.RestrictedLength/2,-self.SmallWidth/2) #Drawing the Horizontal junction
            p1 = gdspy.Polygon(curve.get_points(),layer=self.layer)
            
            
            self.HorizontalCell.add(p1)
            
            return Utility.rotation(self.HorizontalCell, self.coord_x, self.coord_y, self.rotation)
        
        
      def drawVerticalJunction(self):
          
          """
          Class drawing a vertical junction """
          
          curve = gdspy.Curve(-self.LargeWidth/2,0).L(self.LargeWidth/2,0, self.LargeWidth/2,-self.TotalLength/2+2,self.SmallWidth/2,-self.TotalLength/2+1,self.SmallWidth/2,-self.TotalLength/2+1-self.RestrictedLength,-self.SmallWidth/2,-self.TotalLength/2+1-self.RestrictedLength)
          curve.L(-self.SmallWidth/2,-self.TotalLength/2+1,-self.LargeWidth/2,-self.TotalLength/2+2) #Drawing a vertical junction
          p1 = gdspy.Polygon(curve.get_points(),layer=self.layer) 
          
          
          self.VerticalCell.add(p1)
          
          return Utility.rotation(self.VerticalCell, self.coord_x, self.coord_y, self.rotation)
      
      
      def drawSQUID(self,LeftJunctionX,RightJunctionX,DisplacementY):
          
        """
        Class drawing a set of junction (SQUID) """
        
        JunctionSetRotation=self.rotation #Desired rotation for the junctions
        self.rotation=0 #We set the other rotation to 0 to avoid double rotating everything 
        
        
        
        #Set all of the cells to draw the pattern at zero, zero
        HorizontalJunction=gdspy.CellReference(self.drawHorizontalJunction(),origin=(-self.coord_x,-self.coord_y)) # Draws an Horizontal junction centered at the origine
        VerticalJunctionLeft=gdspy.CellReference(self.drawVerticalJunction(),origin=(-LeftJunctionX-self.coord_x,DisplacementY-self.coord_y)) # Draw a junction on the left at position -LeftJunctionX and DisplacementY
        VerticalJunctionRight=gdspy.CellReference(self.drawVerticalJunction(),origin=(RightJunctionX-self.coord_x,DisplacementY-self.coord_y)) # draw a junction on the right at position RightJunctionX and DisplacementY 
        self.DoubleCell.add([ VerticalJunctionLeft, VerticalJunctionRight,HorizontalJunction])
      
        #Rotate the pattern made at zero, zero and then translate it to the desired place in the return function
        RotatedDoubleAngleJunction=gdspy.CellReference(self.DoubleCell, origin=(0,0),rotation=JunctionSetRotation)
        self.cell.add(RotatedDoubleAngleJunction)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y,0 )
    
    
        
      def drawSQUIDUnderCut(self,LeftJunctionX,RightJunctionX,DisplacementY,UnderCutLayer):
            
        """
        Class drawing a set of junction (SQUID) with added undercut opening in MMA"""

        JunctionSetRotation=self.rotation #Desired rotation for the junctions
        self.rotation=0 #We set the other rotation to 0 to avoid double rotating everything 
        
        #Added undercut 
        UnderCutWidth=self.LargeWidth*2
        UnderCutHeight=1
        UnderCut=gdspy.Rectangle((-UnderCutWidth/2,0), (UnderCutWidth/2,UnderCutHeight),layer=UnderCutLayer)
        self.UnderCutCell.add(UnderCut)
        
        #Set all of the cells to draw the pattern at zero, zero
        HorizontalJunction=gdspy.CellReference(self.drawHorizontalJunction(),origin=(-self.coord_x,-self.coord_y)) # Draws an Horizontal junction centered at the origine
        UnderCutHorizontal=gdspy.CellReference(self.UnderCutCell,origin=(-self.TotalLength/2,0),rotation=90)
        VerticalJunctionLeft=gdspy.CellReference(self.drawVerticalJunction(),origin=(-LeftJunctionX-self.coord_x,DisplacementY-self.coord_y)) # Draw a junction on the left at position -LeftJunctionX and DisplacementY
        UnderCutLeft=gdspy.CellReference(self.UnderCutCell,origin=(-LeftJunctionX,DisplacementY))
        VerticalJunctionRight=gdspy.CellReference(self.drawVerticalJunction(),origin=(RightJunctionX-self.coord_x,DisplacementY-self.coord_y)) # draw a junction on the right at position RightJunctionX and DisplacementY 
        UnderCutRight=gdspy.CellReference(self.UnderCutCell,origin=(RightJunctionX,DisplacementY))
        self.DoubleCell.add([ VerticalJunctionLeft, VerticalJunctionRight,HorizontalJunction,UnderCutLeft,UnderCutRight,UnderCutHorizontal])
      
        #Rotate the pattern made at zero, zero and then translate it to the desired place in the return function
        RotatedDoubleAngleJunction=gdspy.CellReference(self.DoubleCell, origin=(0,0),rotation=JunctionSetRotation)
        self.cell.add(RotatedDoubleAngleJunction)
        
        

        
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y,0 )
       
        
       
        
      def drawJunction(self, LeftJunctionX, DisplacementY):
          
        """
        Class drawing a single junction on the left side """
        
        JunctionSetRotation=self.rotation #Desired rotation for the junctions
        self.rotation=0 #We set the other rotation to 0 to avoid double rotating everything 
        
        
        #Set all of the cells to draw the pattern at zero, zero
        HorizontalJunction=gdspy.CellReference(self.drawHorizontalJunction(),origin=(-self.coord_x,-self.coord_y)) # Draws an Horizontal junction centered at the origine
        VerticalJunctionLeft=gdspy.CellReference(self.drawVerticalJunction(),origin=(-LeftJunctionX-self.coord_x,DisplacementY-self.coord_y),rotation=0) # Draw a junction on the left at position -LeftJunctionX and DisplacementY    
        self.DoubleCell.add([HorizontalJunction, VerticalJunctionLeft]) 
        
        
        #Rotate the pattern made at zero, zero and then translate it to the desired place in the return function
        RotatedDoubleAngleJunction=gdspy.CellReference(self.DoubleCell, origin=(0,0),rotation=JunctionSetRotation)
        self.cell.add(RotatedDoubleAngleJunction)
            
        
         
        return Utility.rotation(self.cell,  self.coord_x, self.coord_y,0 )
    
    
        
      def drawJunctionUnderCut(self, LeftJunctionX, DisplacementY,UnderCutLayer):
          
        """
        Class drawing a single junction on the left side """
        
        JunctionSetRotation=self.rotation #Desired rotation for the junctions
        self.rotation=0 #We set the other rotation to 0 to avoid double rotating everything 
        
        #Added undercut 
        UnderCutWidth=self.LargeWidth*2
        UnderCutHeight=1
        UnderCut=gdspy.Rectangle((-UnderCutWidth/2,0), (UnderCutWidth/2,UnderCutHeight),layer=UnderCutLayer)
        self.UnderCutCell.add(UnderCut)
        
        
        #Set all of the cells to draw the pattern at zero, zero
        HorizontalJunction=gdspy.CellReference(self.drawHorizontalJunction(),origin=(-self.coord_x,-self.coord_y)) # Draws an Horizontal junction centered at the origine
        UnderCutHorizontal=gdspy.CellReference(self.UnderCutCell,origin=(-self.TotalLength/2,0),rotation=90)
        VerticalJunctionLeft=gdspy.CellReference(self.drawVerticalJunction(),origin=(-LeftJunctionX-self.coord_x,DisplacementY-self.coord_y),rotation=0) # Draw a junction on the left at position -LeftJunctionX and DisplacementY  
        UnderCutLeft=gdspy.CellReference(self.UnderCutCell,origin=(-LeftJunctionX,DisplacementY))
        self.DoubleCell.add([HorizontalJunction, VerticalJunctionLeft, UnderCutLeft, UnderCutHorizontal]) 
        
        
        #Rotate the pattern made at zero, zero and then translate it to the desired place in the return function
        RotatedDoubleAngleJunction=gdspy.CellReference(self.DoubleCell, origin=(0,0),rotation=JunctionSetRotation)
        self.cell.add(RotatedDoubleAngleJunction)
            
        
         
        return Utility.rotation(self.cell,  self.coord_x, self.coord_y,0 )
        
        

        
        
    
class TestPad:
    """Class for creating Pads for resistance test """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("TestPad")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,Height, Width, ConstrictionWidth, ConstrictionHeight, TaperedWidth, SlotWidth ):
        """
        Height : Height of the Pad
        Width: Width of the straight section of the pad
        ConstrictionWidth : Width of the smaller region of the Pad connected to the device to measure
        ConstrictionHeight : Height of the smaller region of the Pad conencted to the devide to measure
        TaperedHeight : Height of the smaller region of the pad 
        SlotWidth: Opening of the ground plane around the pad
        """
        self.Height=Height
        self.Width=Width
        self.ConstrictionWidth=ConstrictionWidth
        self.ConstrictionHeight=ConstrictionHeight
        self.TaperedWidth=TaperedWidth
        self.SlotWidth=SlotWidth
        
    def draw(self):
        """
        Method for drawing the test Pad
        """
        
       
        #Draws the inner shape of the pad
        curve = gdspy.Curve(0,0).L(self.Width,0, self.Width+self.TaperedWidth,-self.Height/2+self.ConstrictionWidth/2,self.Width+self.TaperedWidth+self.ConstrictionHeight,-self.Height/2+self.ConstrictionWidth/2)
        curve.L(self.Width+self.TaperedWidth+self.ConstrictionHeight,-self.Height/2-self.ConstrictionWidth/2,self.Width+self.TaperedWidth,-self.Height/2-self.ConstrictionWidth/2,self.Width,-self.Height,0,-self.Height )
        p1 = gdspy.Polygon(curve.get_points(),layer=self.layer)
        
        #Creates another pad, but with the size of each side increased by the slotwidth
        OffsetPad=gdspy.offset(p1, self.SlotWidth,layer=self.layer)
        
        #Substrate the inner and outerpad to obtain what is etched in the ground plane
        PadGroundPlane=gdspy.boolean(OffsetPad, p1, "not",layer=self.layer)
        
        #Translate the polygon to set the zeroa
        PadGroundPlane.translate(-self.Width-self.TaperedWidth-self.ConstrictionHeight, self.Height/2)
        
        
        self.cell.add(PadGroundPlane)
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    



class TwoSideTestPad:
    """Class for creating Pads junctions"""
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("TWOSIDESPads")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,Height, Width, ConstrictionWidth, ConstrictionHeight, TaperedWidth, SlotWidth ):
        """
        Height : Height of the Pad
        Width: Width of the straight section of the pad
        ConstrictionWidth : Width of the smaller region of the Pad connected to the device to measure
        ConstrictionHeight : Height of the smaller region of the Pad conencted to the devide to measure
        TaperedHeight : Height of the smaller region of the pad 
        SlotWidth: Opening of the ground plane around the pad
        """
        self.Height=Height
        self.Width=Width/2
        self.ConstrictionWidth=ConstrictionWidth
        self.ConstrictionHeight=ConstrictionHeight
        self.TaperedWidth=TaperedWidth
        self.SlotWidth=SlotWidth
        
    def draw(self,EBL=False):
        """
        Method for drawing the test Pad
        """
        
       
        #Draws the inner shape of the pad
        curve = gdspy.Curve(0,0).L(self.Width,0, self.Width+self.TaperedWidth,-self.Height/2+self.ConstrictionWidth/2,self.Width+self.TaperedWidth+self.ConstrictionHeight,-self.Height/2+self.ConstrictionWidth/2)
        curve.L(self.Width+self.TaperedWidth+self.ConstrictionHeight,-self.Height/2-self.ConstrictionWidth/2,self.Width+self.TaperedWidth,-self.Height/2-self.ConstrictionWidth/2,self.Width,-self.Height,0,-self.Height)
        curve.L(-self.Width,-self.Height,-self.Width-self.TaperedWidth,-self.Height/2-self.ConstrictionWidth/2,-self.Width-self.TaperedWidth-self.ConstrictionHeight,-self.Height/2-self.ConstrictionWidth/2,-self.Width-self.TaperedWidth-self.ConstrictionHeight,-self.Height/2+self.ConstrictionWidth/2)
        curve.L(-self.Width-self.TaperedWidth,-self.Height/2+self.ConstrictionWidth/2,-self.Width,0)
        
        p1 = gdspy.Polygon(curve.get_points(),layer=self.layer)
        
        #Creates another pad, but with the size of each side increased by the slotwidth
        OffsetPad=gdspy.offset(p1, self.SlotWidth,layer=self.layer)
        
        if EBL==False:
            #Substrate the inner and outerpad to obtain what is etched in the ground plane
            PadGroundPlane=gdspy.boolean(OffsetPad, p1, "not",layer=self.layer)
        else :
            PadGroundPlane=p1
        
        #Translate the polygon to set the zeroa
        PadGroundPlane.translate(-self.Width-self.TaperedWidth-self.ConstrictionHeight, self.Height/2)
        
        
        self.cell.add(PadGroundPlane)
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        
    
    
    
        


            