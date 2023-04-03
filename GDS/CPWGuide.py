# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 13:27:20 2022


Module for creating a CPW and adding the different types of termination and object to it.

@author: beaulieu
"""

import gdspy
from GDS import Utility 
import numpy as np
from GDS import Termination as Term 



class CPWGuide:
    """
    Class for creating coplanar wave guide paths 
    """
    
    
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("CPWGUIDE")
        
        
        self.EndCoordinate=(0,0) # Set of coordinates of the path's end
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
    def setParameters(self,StripWidth,SlotWidth):
        """
        StripWidth : Width of the conducting region of the CPW
        SlotWidth : Width of the spcaing between the conducting channel and the groumd
        """
        self.StripWidth=StripWidth
        self.SlotWidth=SlotWidth
        
        
    def SetPoint(self,coord_x,coord_y):
        
        """
        Defines a new set point to continue writing the termination and other elements. 
        """
        #self.coord_x=0
        #self.coord_y=0
        
        self.EndCoordinate=(coord_x-self.coord_x, coord_y-self.coord_y)
       
    
    
    def RelSetPoint(self,delta_x,delta_y):
        """
        Translates the set point by delta_x and delta_y 
        """
        
        self.EndCoordinate=(self.EndCoordinate[0]+delta_x, self.EndCoordinate[1]+delta_y)
       
        
    def drawStraight(self,Length,Direction):
        """
        Method allowing to draw a straight CPW 
        
        Length : Number giving the length of the CPW 
        Direction : "+x","-x","+y" or "-y" giving the diretion in which the waveguide goes
        
        """
        
        
        
        #Draw the waveguide using the path tool
        CPWPath = gdspy.Path(self.SlotWidth,initial_point=self.EndCoordinate, number_of_paths=2, distance = self.SlotWidth + self.StripWidth)
        CPWPath.segment(Length,Direction,layer=self.layer)
        
        #Saves the new end coordinates
        self.EndCoordinate=(CPWPath.x,CPWPath.y) # Update Coordinates
        
        #Add element to cell 
        self.cell.add(CPWPath)

        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    
    
    def drawTurn(self,radius,angle,direction):
        """
        Method allowing to draw a turn in the CPW (following the previously defined path)
        
        Radius : Radius of the turn 
        Angle : "r", "rr", "l" or "ll" where "r" stand for a right turn and "l" for a left turn of 90 degrees. For 180 degree
        turns, the double letter is used. The direction of the turn is defined following the path of the waveguide
        direction : "+x","-x","+y" or "-y" giving thecurrent direction of the wave guide 
        """
      
        
        #Defines the waveguide using the path tool
        CPWPath = gdspy.Path(self.SlotWidth,initial_point=self.EndCoordinate, number_of_paths=2, distance = self.SlotWidth + self.StripWidth)
        
        
        #This is a necessary correction for the turn to always follow the path no matter its direction
        _halfpi=np.pi/2
        
        if angle == "r":
            delta_i = _halfpi
            delta_f = 0
        elif angle == "rr":
            delta_i = _halfpi
            delta_f = -delta_i
        elif angle == "l":
            delta_i = -_halfpi
            delta_f = 0
        elif angle == "ll":
            delta_i = -_halfpi
            delta_f = -delta_i
        elif angle < 0:
            exact = False
            delta_i = _halfpi
            delta_f = delta_i + angle
        else:
            exact = False
            delta_i = -_halfpi
            delta_f = delta_i + angle
            
        if direction == "+x":
            direction = 0
        elif direction == "-x":
            direction = np.pi
        elif direction == "+y":
            direction = _halfpi
        elif direction == "-y":
            direction = -_halfpi
        elif exact:
            exact = False
        
        #The turn is added to the path
        CPWPath.arc(radius,direction + delta_i, direction + delta_f,layer=self.layer)
        
        #EndCoordinates are updated 
        self.EndCoordinate=(CPWPath.x,CPWPath.y)
        #Add element to cell 
        self.cell.add(CPWPath)
   
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
        
    
    
    def ConnectObject(self,Object, Direction):
        """
        Method allowing to connect a waveguide with its terminations to another object
        
        Object : an object that belongs to a class that should have already been created in the script 
        Direction :  "+x","-x","+y" or "-y" giving the direction in which to add the termination """
        
        
        
       
        #For the Xmon class
        if Object.__class__.__name__ =="Xmon":
            
          
            #For each element, we add the object in the correct direction and update the reference coordinates of the object
            
            if Direction=="+x":
                TransformedObj=Utility.rotation(Object.cell, self.EndCoordinate[0]+Object.CrossLength/2+Object.SlotWidth, self.EndCoordinate[1], 0)
                self.cell.add(TransformedObj)
                
                
                
                Object.RightCoordinate=(self.EndCoordinate[0]+Object.CrossLength+Object.SlotWidth*2+self.coord_x,self.EndCoordinate[1]+self.coord_y)
                Object.BottomCoordinate=(self.EndCoordinate[0]+Object.CrossLength/2+Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y-Object.CrossLength/2-Object.SlotWidth)
                Object.TopCoordinate=(self.EndCoordinate[0]+Object.CrossLength/2+Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y+Object.CrossLength/2+Object.SlotWidth)
            
            elif Direction=="-x":
                TransformedObj=Utility.rotation(Object.cell, self.EndCoordinate[0]-Object.CrossLength/2-Object.SlotWidth, self.EndCoordinate[1], 0)
                self.cell.add(TransformedObj)
                
                
                Object.LeftCoordinate=(self.EndCoordinate[0]-Object.CrossLength-Object.SlotWidth*2+self.coord_x,self.EndCoordinate[1]+self.coord_y)
                Object.BottomCoordinate=(self.EndCoordinate[0]-Object.CrossLength/2-Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y-Object.CrossLength/2-Object.SlotWidth)
                Object.TopCoordinate=(self.EndCoordinate[0]-Object.CrossLength/2-Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y+Object.CrossLength/2+Object.SlotWidth)
            
             
            elif Direction=="-y":
                TransformedObj=Utility.rotation(Object.cell, self.EndCoordinate[0], self.EndCoordinate[1]-Object.CrossLength/2-Object.SlotWidth, 0)
                self.cell.add(TransformedObj)
                
                
                Object.LeftCoordinate=(self.EndCoordinate[0]-Object.CrossLength/2-Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y-Object.CrossLength/2-Object.SlotWidth)
                Object.BottomCoordinate=(self.EndCoordinate[0]+self.coord_x,self.EndCoordinate[1]+self.coord_y-Object.CrossLength-Object.SlotWidth*2)
                Object.RightCoordinate=(self.EndCoordinate[0]+Object.CrossLength/2+Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y-Object.CrossLength/2-Object.SlotWidth)
              
            
             
            elif Direction=="+y":
                TransformedObj=Utility.rotation(Object.cell, self.EndCoordinate[0], self.EndCoordinate[1]+Object.CrossLength/2+Object.SlotWidth, 0)
                self.cell.add(TransformedObj)
                
                Object.LeftCoordinate=(self.EndCoordinate[0]-Object.CrossLength/2-Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y+Object.CrossLength/2+Object.SlotWidth)
                Object.BottomCoordinate=(self.EndCoordinate[0]+self.coord_x,self.EndCoordinate[1]+self.coord_y+Object.CrossLength+Object.SlotWidth*2)
                Object.RightCoordinate=(self.EndCoordinate[0]+Object.CrossLength/2+Object.SlotWidth+self.coord_x,self.EndCoordinate[1]+self.coord_y+Object.CrossLength/2+Object.SlotWidth)
          
          
           
            
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)    
        
    
    
    
    
    
    def drawTermination(self,Termination,Direction,layer,Reversed=False):
        """
        Method allowing to draw a termination to the waveguide
        
        Termination : Dictionnary object with the key corresponding to the type of termination and the item being a list of the required 
        parameters to draw it: 
        
            Termination={"Pad", [PadWidth,OffsetPadEtch,PadLength,ImpMatchLength]}
            Termination={"CPWOpening":[OpeningWidth, OpeningLength]}
            
            
            
            
        Direction :  "+x","-x","+y" or "-y" giving the direction in which adding the termination
        """
          
        #List of the keys in dictionnary
        keys=list(Termination.keys())[0]
             
        
        if keys=="CPWPad":
            #Termination={"Pad", [PadWidth,OffsetPadEtch,PadLength,ImpMatchLength]} 
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["CPWPad"][1]+Termination["CPWPad"][2]+Termination["CPWPad"][3] #Distance to Update the final point
        
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
               Direction=180
               self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
               if Reversed==True :
                   (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                   self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
               
            #Draw and add the element
            Pad=Term.CPWPad(RedPointX,RedPointY,Direction,layer)
            Pad.setParameters(Termination["CPWPad"][0], Termination["CPWPad"][1], Termination["CPWPad"][2], Termination["CPWPad"][3], self.StripWidth, self.SlotWidth)
            self.cell.add(Pad.draw())
            
            
            
   
        elif keys=="CPWOpening":
            # Termination={"CPWOpening":[OpeningWidth, OpeningLength]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["CPWOpening"][1] #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint.
            if Direction=="+x":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance, self.EndCoordinate[1])
            elif Direction=="-y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]-BluePointDistance)
            elif Direction=="+y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]+BluePointDistance)
            elif Direction=="-x":
               Direction=180
               self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance, self.EndCoordinate[1])
            
            #Draw and add the element
            Opening=Term.CPWOpening(RedPointX,RedPointY,Direction,layer)
            Opening.setParameters(Termination["CPWOpening"][0],Termination["CPWOpening"][1])
            self.cell.add(Opening.draw())
            
            
            
       
        elif keys=="CPWQubitCoupling":
            #Termination={"CPWQubitCoupling":[CentralConductorWidth,SideConductorWidth,SideLength]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=self.SlotWidth*2+self.StripWidth #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance, self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=0 
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
               Direction=-90
               self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance, self.EndCoordinate[1])
               if Reversed==True :
                   (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                   self.EndCoordinate=(RedPointX,RedPointY)
               
            #Draw and add the element
            QbitCoupling=Term.CPWQubitCoupling(RedPointX,RedPointY,Direction,layer)
            QbitCoupling.setParameters(Termination["CPWQubitCoupling"][0], Termination["CPWQubitCoupling"][1], Termination["CPWQubitCoupling"][2],self.StripWidth, self.SlotWidth)
            self.cell.add(QbitCoupling.draw())
            
            
        
        elif keys=="CPWQubitDriveLine":
            #TerminationQubitDrive={"QubitDriveLine":[FinStripWidth,FinSlotWidth,TaperedLength,StraightLength]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["CPWQubitDriveLine"][2]+Termination["CPWQubitDriveLine"][3]+Termination["CPWQubitDriveLine"][1] #Distance to Update the final point
           
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance, self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
                
            elif Direction=="-x":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance, self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
                
            elif Direction=="-y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
                
            #Draw and add the element
            DriveLine=Term.CPWQubitDriveLine(RedPointX,RedPointY,Direction,layer)
            DriveLine.setParameters(self.StripWidth, self.SlotWidth, Termination["CPWQubitDriveLine"][0],Termination["CPWQubitDriveLine"][1],Termination["CPWQubitDriveLine"][2],Termination["CPWQubitDriveLine"][3])
            self.cell.add(DriveLine.draw())
        
        
        
        elif keys=="CPWFluxLine":
            #TerminationFluxLine={"CPWFluxLine":[FinStripWidth, FinSlotWidth, TaperedLength, StraightLength, Gap, OpeningLength, OpeningOffset]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["CPWFluxLine"][2]+Termination["CPWFluxLine"][3]+Termination["CPWFluxLine"][1] #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=0       
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance, self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance, self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0], self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
                
            #Draw and add the element
            Line=Term.CPWFluxLine(RedPointX,RedPointY,Direction,layer)
            Line.setParameters(self.StripWidth, self.SlotWidth, Termination["CPWFluxLine"][0], Termination["CPWFluxLine"][1],Termination["CPWFluxLine"][2],Termination["CPWFluxLine"][3],Termination["CPWFluxLine"][4],Termination["CPWFluxLine"][5],Termination["CPWFluxLine"][6])
            self.cell.add(Line.draw())
            
        
        
        
       
        elif keys=="TPatch":
            #TerminationTPatch={"TPatch":[TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["TPatch"][4] #Distance to Update the final point
         
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":      
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
                    
                
            #Draw and add the element        
            Patch=Term.TPatch(RedPointX,RedPointY,Direction,layer)
            Patch.setParameters(Termination["TPatch"][0], Termination["TPatch"][1], Termination["TPatch"][2], Termination["TPatch"][3], Termination["TPatch"][4], Termination["TPatch"][5])
            self.cell.add(Patch.draw())
            
        
            
            
        elif keys=="UPatch":
            #TerminationUPatch={"UPatch":[SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["UPatch"][3] #Distance to Update the final point
            
           
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
               Direction=-90
               self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
               if Reversed==True :
                   (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
               
            #Draw and add the element  
            Patch=Term.UPatch(RedPointX,RedPointY,Direction,layer)
            Patch.setParameters(Termination["UPatch"][0], Termination["UPatch"][1], Termination["UPatch"][2], Termination["UPatch"][3],Termination["UPatch"][4])
            self.cell.add(Patch.draw())
            
            
            
        elif keys=="JunctionDoubleAngle": 
            #TerminationJunction={"JunctionDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=(Termination["JunctionDoubleAngle"][0]/2-Termination["JunctionDoubleAngle"][5]+Termination["JunctionDoubleAngle"][3]-3) #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                RedPointX=RedPointX+Termination["JunctionDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX-Termination["JunctionDoubleAngle"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                RedPointX=RedPointX-Termination["JunctionDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX+Termination["JunctionDoubleAngle"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                RedPointY=self.EndCoordinate[1]+Termination["JunctionDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY-Termination["JunctionDoubleAngle"][0]/2)
            elif Direction=="-y":
                Direction=0
                RedPointY=self.EndCoordinate[1]-Termination["JunctionDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY+Termination["JunctionDoubleAngle"][0]/2)
            
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["JunctionDoubleAngle"][0],Termination["JunctionDoubleAngle"][1],Termination["JunctionDoubleAngle"][2],Termination["JunctionDoubleAngle"][3])
            self.cell.add(Junctions.drawJunction(Termination["JunctionDoubleAngle"][4],Termination["JunctionDoubleAngle"][5]))
   
            
   
    
        elif keys=="JunctionDoubleAngleUnderCut": 
            #TerminationJunction={"JunctionDoubleAngleUnderCut":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY,UnderCutLayer]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=(Termination["JunctionDoubleAngleUnderCut"][0]/2-Termination["JunctionDoubleAngleUnderCut"][5]+Termination["JunctionDoubleAngleUnderCut"][3]-3) #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                RedPointX=RedPointX+Termination["JunctionDoubleAngleUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX-Termination["JunctionDoubleAngleUnderCut"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                RedPointX=RedPointX-Termination["JunctionDoubleAngleUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX+Termination["JunctionDoubleAngleUnderCut"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                RedPointY=self.EndCoordinate[1]+Termination["JunctionDoubleAngleUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY-Termination["JunctionDoubleAngleUnderCut"][0]/2)
            elif Direction=="-y":
                Direction=0
                RedPointY=self.EndCoordinate[1]-Termination["JunctionDoubleAngleUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY+Termination["JunctionDoubleAngleUnderCut"][0]/2)
            
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["JunctionDoubleAngleUnderCut"][0],Termination["JunctionDoubleAngleUnderCut"][1],Termination["JunctionDoubleAngleUnderCut"][2],Termination["JunctionDoubleAngleUnderCut"][3])
            self.cell.add(Junctions.drawJunctionUnderCut(Termination["JunctionDoubleAngleUnderCut"][4],Termination["JunctionDoubleAngleUnderCut"][5],Termination["JunctionDoubleAngleUnderCut"][6]))
             
       
        elif keys=="SQUIDDoubleAngle":
            #TerminationDoubleJunction={"SQUID":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=(Termination["SQUIDDoubleAngle"][3]-3-Termination["SQUIDDoubleAngle"][6]+Termination["SQUIDDoubleAngle"][0]/2) #Distance to Update the final point
            
           #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                RedPointX=RedPointX+Termination["SQUIDDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]+ BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX-Termination["SQUIDDoubleAngle"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                RedPointX=RedPointX-Termination["SQUIDDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]- BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=180
                RedPointY=RedPointY+Termination["SQUIDDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+ BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY-Termination["SQUIDDoubleAngle"][0]/2)
            elif Direction=="-y":
                Direction=0
                RedPointY=RedPointY-Termination["SQUIDDoubleAngle"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]- BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY+Termination["SQUIDDoubleAngle"][0]/2)
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["SQUIDDoubleAngle"][0],Termination["SQUIDDoubleAngle"][1],Termination["SQUIDDoubleAngle"][2],Termination["SQUIDDoubleAngle"][3])
            self.cell.add(Junctions.drawSQUID(Termination["SQUIDDoubleAngle"][4],Termination["SQUIDDoubleAngle"][5],Termination["SQUIDDoubleAngle"][6]))
            
            
            
            
        
            
        
        elif keys=="SQUIDDoubleAngleJunctionUnderCut":
         #{"DoubleAngleJunctionUnderCut":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY,LayerUnderCut]}    

            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=(Termination["SQUIDDoubleAngleJunctionUnderCut"][3]-3-Termination["SQUIDDoubleAngleJunctionUnderCut"][6]+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)#Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                RedPointX=RedPointX+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                RedPointX=RedPointX-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                RedPointY=self.EndCoordinate[1]+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
            elif Direction=="-y":
                Direction=0
                RedPointY=self.EndCoordinate[1]-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
            
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["SQUIDDoubleAngleJunctionUnderCut"][0],Termination["SQUIDDoubleAngleJunctionUnderCut"][1],Termination["SQUIDDoubleAngleJunctionUnderCut"][2],Termination["SQUIDDoubleAngleJunctionUnderCut"][3])
            self.cell.add(Junctions.drawSQUIDUnderCut(Termination["SQUIDDoubleAngleJunctionUnderCut"][4],Termination["SQUIDDoubleAngleJunctionUnderCut"][5],Termination["SQUIDDoubleAngleJunctionUnderCut"][6],Termination["SQUIDDoubleAngleJunctionUnderCut"][7]))
       
        
       
        elif keys=="TestPad":
            #{"TestPad":[Height,Width,ConstrictionWidth,ConstrictionHeight,TaperedWidth]}
           
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
            BluePointDistance=Termination["TestPad"][1]+Termination["TestPad"][4]+Termination["TestPad"][3]+self.SlotWidth
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
    
    
            #Draw and add the element 
            Pad=Term.TestPad(RedPointX,RedPointY,Direction,layer)
            Pad.setParameters(Termination["TestPad"][0],Termination["TestPad"][1],Termination["TestPad"][2],Termination["TestPad"][3],Termination["TestPad"][4],self.SlotWidth)
            self.cell.add(Pad.draw())
            
        elif keys=="TwoSideTestPad":
            #{"TwoSideTestPad":[Height,Width,ConstrictionWidth,ConstrictionHeight,TaperedWidth]}
            
            (RedPointX,RedPointY)= (self.EndCoordinate[0],self.EndCoordinate[1]) #Defines the inital red point
          
            BluePointDistance=Termination["TwoSideTestPad"][1]+Termination["TwoSideTestPad"][4]*2 +Termination["TwoSideTestPad"][3]*2
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=180
                self.EndCoordinate=(self.EndCoordinate[0]+BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="+y":
                Direction=-90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-x":
                Direction=0
                self.EndCoordinate=(self.EndCoordinate[0]-BluePointDistance,self.EndCoordinate[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinate=(RedPointX,RedPointY)
            elif Direction=="-y":
                Direction=90
                self.EndCoordinate=(self.EndCoordinate[0],self.EndCoordinate[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinate=(RedPointX,RedPointY)
    
    
            #Draw and add the element 
            Pad=Term.TwoSideTestPad(RedPointX,RedPointY,Direction,layer)
            Pad.setParameters(Termination["TwoSideTestPad"][0],Termination["TwoSideTestPad"][1],Termination["TwoSideTestPad"][2],Termination["TwoSideTestPad"][3],Termination["TwoSideTestPad"][4],self.SlotWidth)
            self.cell.add(Pad.draw(EBL=True))
            
            
            
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
                 
                    
                    
                
 