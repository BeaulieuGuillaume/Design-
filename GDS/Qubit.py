# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:52:45 2022

@author: beaulieu
"""

import gdspy
from GDS import Utility
import numpy as np
from GDS import Termination as Term


class Xmon:
    """
    Class for creating a Qubit 
    """
    
    def __init__(self, coord_x, coord_y, rotation,layer):
        
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("XMON")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.layer=layer
        self.cell = cell
        self.lib = lib
        
        
        
    def setParameters(self,StripWidth,SlotWidth, CrossLength):
        """
        StripWidth : Width of the conducting region of the QUBIT
        SlotWidth : Width of the spcaing between the conducting channel and the groumd
        CrossLength : Length of one side of the cross
        """
            
        self.StripWidth=StripWidth
        self.SlotWidth=SlotWidth
        self.CrossLength=CrossLength
        
        
        ArmLength=(self.CrossLength-self.StripWidth)/2 #Defines the arm length
        
        # Set the coordinates at the end of each arm
        self.TopCoordinate=(self.coord_x,ArmLength+self.StripWidth/2+self.coord_y) 
        self.BottomCoordinate=(self.coord_x,-ArmLength-self.StripWidth/2+self.coord_y)
        self.RightCoordinate=(ArmLength+self.StripWidth/2+self.coord_x,self.coord_y)
        self.LeftCoordinate=(-ArmLength-self.StripWidth/2+self.coord_x,self.coord_y)
        
        #Coordiantes that will be updated 
        self.EndCoordinateRight=self.RightCoordinate
        self.EndCoordinateBottom=self.BottomCoordinate
        self.EndCoordinateTop=self.TopCoordinate
        self.EndCoordinateLeft=self.LeftCoordinate
        
        
    def RelSetPoint(self,Direction,delta_x,delta_y):
        """
        Translates the set point in a certain direction by delta_x and delta_y 
        """
        
        if Direction=="+x":
           self.EndCoordinateRight=(self.EndCoordinateRight[0]+delta_x, self.EndCoordinateRight[1]+delta_y)
        
        elif Direction=="-x":
            self.EndCoordinateLeft=(self.EndCoordinateLeft[0]+delta_x, self.EndCoordinateLeft[1]+delta_y)
        
        elif Direction=="-y":
            self.EndCoordinateBottom=(self.EndCoordinateBottom[0]+delta_x, self.EndCoordinateBottom[1]+delta_y)
        
        elif Direction=="+y":
            self.EndCoordinateTop=(self.EndCoordinateTop[0]+delta_x, self.EndCoordinateTop[1]+delta_y)
        
        
        
    def draw(self):
        
        """
        Method allowing to draw the cross of the XMON
        """
        
        ArmLength=(self.CrossLength-self.StripWidth)/2 #Defines the arm length
        
        #Draw the inner conductor
        curve = gdspy.Curve(0, 0).L(ArmLength,0, ArmLength,-ArmLength, ArmLength+self.StripWidth,-ArmLength, ArmLength+self.StripWidth,0,self.CrossLength,0,self.CrossLength,self.StripWidth, ArmLength+self.StripWidth, self.StripWidth)
        curve.L(ArmLength+self.StripWidth,ArmLength+self.StripWidth, ArmLength, self.StripWidth+ArmLength, ArmLength, self.StripWidth,0, self.StripWidth)
        p1 = gdspy.Polygon(curve.get_points(),layer=self.layer)
        
        #Create an offset polygon and substract to obtain only the qubit
        p2=gdspy.offset(p1, self.SlotWidth,layer=self.layer)
        p3=gdspy.boolean(p2, p1, "not",layer=self.layer) 
        
        #Add with the cross centered at zero
        self.cell.add(p3.translate(-ArmLength-self.StripWidth/2, -self.StripWidth/2))
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
     
    def drawTermination(self,Termination,Direction,layer,Reversed=False):
        """
        Method allowing to draw a termination to the waveguide
        
        Termination : Dictionnary object with the key corresponding to the type of termination and the item being a list of the required 
        parameters to draw it. 
            Termination={"Pad", [PadWidth,OffsetPadEtch,PadLength,ImpMatchLength]}
            Termination={"TPatch":[TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight,Overlap]}
        Direction :  "+x","-x","+y" or "-y" giving the direction in which adding the termination
        """
          
        keys=list(Termination.keys())[0]
            
        if keys=="UPatch": 
            #TerminationUPatch={"UPatch":[SideWidth, BottomHeight, RadiusCorner, SideHeight, TotalWidth]}
           
            BluePointDistance=Termination["UPatch"][3]
            
            if Direction=="+x":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0],self.EndCoordinateRight[1]) #Defines the inital red point
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1])
                if Reversed==True :
                      (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                      self.EndCoordinateRight=(RedPointX,RedPointY)
                    
            elif Direction=="-y":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]) #Defines the inital red point
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY)
                  
               
            elif Direction=="+y":
                Direction=180
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1])
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY)
    
            elif Direction=="-x":
               Direction=-90
               (RedPointX,RedPointY)= (self.EndCoordinateLeft[0],self.EndCoordinateLeft[1])
               self.EndCoordinateLeft=(self.EndCoordinateLeft[0]-BluePointDistance,self.EndCoordinateLeft[1])
               if Reversed==True :
                   (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                   self.EndCoordinateLeft=(RedPointX,RedPointY)
               
              
             #Draw and add the element 
            Patch=Term.UPatch(RedPointX,RedPointY,Direction,layer)
            Patch.setParameters(Termination["UPatch"][0], Termination["UPatch"][1], Termination["UPatch"][2], Termination["UPatch"][3],Termination["UPatch"][4])
            self.cell.add(Patch.draw())
            
        
        elif keys=="TPatch":
            #TerminationTPatch={"TPatch":[TotalWidth,PartialHeight,TopWidth,RadiusCorner,TotalHeight,TopHeight]}
            
            BluePointDistance=Termination["TPatch"][4] #Distance to Update the final point
            
            if Direction=="+x":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0],self.EndCoordinateRight[1]) #Defines the inital red point
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinateRight=(RedPointX,RedPointY)
                  
            elif Direction=="-y":
                Direction=-90
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]) #Defines the inital red point
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY)
               
            elif Direction=="+y":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1])
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY)
    
            elif Direction=="-x":
               Direction=180
               (RedPointX,RedPointY)= (self.EndCoordinateLeft[0],self.EndCoordinateLeft[1])
               self.EndCoordinateLeft=(self.EndCoordinateLeft[0]-BluePointDistance,self.EndCoordinateLeft[1])
               if Reversed==True :
                   (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                   self.EndCoordinateLeft=(RedPointX,RedPointY)
               
            
            #Draw and add the element 
            Patch=Term.TPatch(RedPointX,RedPointY,Direction,layer)
            Patch.setParameters(Termination["TPatch"][0], Termination["TPatch"][1], Termination["TPatch"][2], Termination["TPatch"][3], Termination["TPatch"][4], Termination["TPatch"][5])
            self.cell.add(Patch.draw())
            
            
            
            
        elif keys=="SQUIDDoubleAngle": 
            #{"SQUIDDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY]}
            
            BluePointDistance=Termination["SQUIDDoubleAngle"][0]/2-Termination["SQUIDDoubleAngle"][5]+Termination["SQUIDDoubleAngle"][3]
           
            if Direction=="+x":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0]+Termination["SQUIDDoubleAngle"][0]/2,self.EndCoordinateRight[1]) #Defines the inital red point
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1]) 
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinateRight=(RedPointX-Termination["SQUIDDoubleAngle"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                (RedPointX,RedPointY)= (self.EndCoordinateLeft[0]-Termination["SQUIDDoubleAngle"][0]/2,self.EndCoordinateLeft[1])
                self.EndCoordinateLeft=(self.EndCoordinateLeft[0]-BluePointDistance,self.EndCoordinateLeft[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinateLeft=(RedPointX+Termination["SQUIDDoubleAngle"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1]+Termination["SQUIDDoubleAngle"][0]/2)
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY+Termination["SQUIDDoubleAngle"][0]/2)
            elif Direction=="-y":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-Termination["SQUIDDoubleAngle"][0]/2)
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY-Termination["SQUIDDoubleAngle"][0]/2)
            
            #Draw and add the element 
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["SQUIDDoubleAngle"][0],Termination["SQUIDDoubleAngle"][1],Termination["SQUIDDoubleAngle"][2],Termination["SQUIDDoubleAngle"][3])
            self.cell.add(Junctions.drawSQUID(Termination["SQUIDDoubleAngle"][4],Termination["SQUIDDoubleAngle"][5],Termination["SQUIDDoubleAngle"][6]))
            
    
         
        elif keys=="JunctionDoubleAngle": 
            #TerminationJunction={"JunctionDoubleAngle":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY]}
            
            #Defines the inital red point
            BluePointDistance=(Termination["JunctionDoubleAngle"][0]/2-Termination["JunctionDoubleAngle"][5]+Termination["JunctionDoubleAngle"][3]-3) #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0]+Termination["JunctionDoubleAngle"][0]/2,self.EndCoordinateRight[1]) 
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinateRight=(RedPointX-Termination["JunctionDoubleAngle"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                (RedPointX,RedPointY)= (self.EndCoordinateLeft[0]-Termination["JunctionDoubleAngle"][0]/2,self.EndCoordinateLeft[1]) 
                self.EndCoordinateLeft=(self.EndCoordinaterLeft[0]+BluePointDistance,self.EndCoordinateLeft[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinateLeft=(RedPointX+Termination["JunctionDoubleAngle"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1]+Termination["JunctionDoubleAngle"][0]/2) 
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY-Termination["JunctionDoubleAngle"][0]/2)
            elif Direction=="-y":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-Termination["JunctionDoubleAngle"][0]/2) 
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY+Termination["JunctionDoubleAngle"][0]/2)
            
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["JunctionDoubleAngle"][0],Termination["JunctionDoubleAngle"][1],Termination["JunctionDoubleAngle"][2],Termination["JunctionDoubleAngle"][3])
            self.cell.add(Junctions.drawJunction(Termination["JunctionDoubleAngle"][4],Termination["JunctionDoubleAngle"][5]))
        
        
              
        elif keys=="SQUIDDoubleAngleJunctionUnderCut": 
            #{""SQUIDDoubleAngleJunctionUnderCut"":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,RightJunctionX,DisplacementY,LayerUnderCut]} 
            
            BluePointDistance=(Termination["SQUIDDoubleAngleJunctionUnderCut"][3]-3-Termination["SQUIDDoubleAngleJunctionUnderCut"][6]+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)#Distance to Update the final point
           
            if Direction=="+x":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0]+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,self.EndCoordinateRight[1]) #Defines the inital red point
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1]) 
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinateRight=(RedPointX-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                (RedPointX,RedPointY)= (self.EndCoordinateLeft[0]-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,self.EndCoordinateLeft[1])
                self.EndCoordinateLeft=(self.EndCoordinateLeft[0]-BluePointDistance,self.EndCoordinateLeft[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinateLeft=(RedPointX+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1]+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
            elif Direction=="-y":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY+Termination["SQUIDDoubleAngleJunctionUnderCut"][0]/2)
            
            #Draw and add the element 
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["SQUIDDoubleAngleJunctionUnderCut"][0],Termination["SQUIDDoubleAngleJunctionUnderCut"][1],Termination["SQUIDDoubleAngleJunctionUnderCut"][2],Termination["SQUIDDoubleAngleJunctionUnderCut"][3])
            self.cell.add(Junctions.drawSQUIDUnderCut(Termination["SQUIDDoubleAngleJunctionUnderCut"][4],Termination["SQUIDDoubleAngleJunctionUnderCut"][5],Termination["SQUIDDoubleAngleJunctionUnderCut"][6],Termination["SQUIDDoubleAngleJunctionUnderCut"][7]))
        
        
        elif keys=="JunctionDoubleAngleUnderCut": 
            #TerminationJunction={"JunctionDoubleAngleUnderCut":[SmallWidth,LargeWidth,RestrictedLength,TotalLength,LeftJunctionX,DisplacementY,UnderCutLayer]}
            
            #Defines the inital red point
            BluePointDistance=(Termination["JunctionDoubleAngleUnderCut"][0]/2-Termination["JunctionDoubleAngleUnderCut"][5]+Termination["JunctionDoubleAngleUnderCut"][3]-3) #Distance to Update the final point
            
            #Place correct orientation and update the bluepoint. Also switch the points if revered
            if Direction=="+x":
                Direction=90
                (RedPointX,RedPointY)= (self.EndCoordinateRight[0]+Termination["JunctionDoubleAngleUnderCut"][0]/2,self.EndCoordinateRight[1]) 
                self.EndCoordinateRight=(self.EndCoordinateRight[0]+BluePointDistance,self.EndCoordinateRight[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX-BluePointDistance,RedPointY)
                    self.EndCoordinateRight=(RedPointX-Termination["JunctionDoubleAngleUnderCut"][0]/2,RedPointY)
            elif Direction=="-x":
                Direction=-90
                (RedPointX,RedPointY)= (self.EndCoordinateLeft[0]-Termination["JunctionDoubleAngleUnderCut"][0]/2,self.EndCoordinateLeft[1]) 
                self.EndCoordinateLeft=(self.EndCoordinaterLeft[0]+BluePointDistance,self.EndCoordinateLeft[1])
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX+BluePointDistance,RedPointY)
                    self.EndCoordinateLeft=(RedPointX+Termination["JunctionDoubleAngleUnderCut"][0]/2,RedPointY)
            elif Direction=="+y":
                Direction=180
                (RedPointX,RedPointY)= (self.EndCoordinateTop[0],self.EndCoordinateTop[1]+Termination["JunctionDoubleAngleUnderCut"][0]/2) 
                self.EndCoordinateTop=(self.EndCoordinateTop[0],self.EndCoordinateTop[1]+BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY-BluePointDistance)
                    self.EndCoordinateTop=(RedPointX,RedPointY-Termination["JunctionDoubleAngleUnderCut"][0]/2)
            elif Direction=="-y":
                Direction=0
                (RedPointX,RedPointY)= (self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-Termination["JunctionDoubleAngleUnderCut"][0]/2) 
                self.EndCoordinateBottom=(self.EndCoordinateBottom[0],self.EndCoordinateBottom[1]-BluePointDistance)
                if Reversed==True :
                    (RedPointX,RedPointY)=(RedPointX,RedPointY+BluePointDistance)
                    self.EndCoordinateBottom=(RedPointX,RedPointY+Termination["JunctionDoubleAngleUnderCut"][0]/2)
            
            
            #Draw and add the element  
            Junctions=Term.DoubleAngleJunction(RedPointX,RedPointY,Direction,layer)
            Junctions.setParameters(Termination["JunctionDoubleAngleUnderCut"][0],Termination["JunctionDoubleAngleUnderCut"][1],Termination["JunctionDoubleAngleUnderCut"][2],Termination["JunctionDoubleAngleUnderCut"][3])
            self.cell.add(Junctions.drawJunctionUnderCut(Termination["JunctionDoubleAngleUnderCut"][4],Termination["JunctionDoubleAngleUnderCut"][5],Termination["JunctionDoubleAngleUnderCut"][6]))
        
      
            
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    