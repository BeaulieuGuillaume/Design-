# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 18:33:45 2022

@author: beaulieu
"""

import gdspy
import numpy as np
from GDS import Utility



class Wafer4:
    
    """Class that draws a 4 inch Wafer with standard dimensions i.e bottom flat 32.5 mm and left flat 18 mm. 
    The class is created with the desired coordinates in x,y and rotation. """
    
    
    def __init__(self, coord_x, coord_y, rotation,layer,RectangleLayer=50):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("WAFER4")
        cellRect =lib.new_cell("RECTANGLES")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell
        self.cellRect=cellRect
        self.layer=layer
        self.RectangleLayer=RectangleLayer
       
    
    def drawWafer4(self):
        """Method to draw the 4 inch wafer. """
        
        #Path linking the right side of the wafer to the left flat
        path1=gdspy.Path(1,(50000,0))
        path1.arc(50000, 0,2.960604715411,layer=self.layer)
        
        #left flat of the wafer
        path2=gdspy.Path(1,(-49183.3172, 9000))
        path2.segment(18000,"-y",layer=self.layer)
        
        
        
        #Path linking the right of the wafer to the bottom flat
        path3=gdspy.Path(1,(50000,0))
        path3.arc(50000, 0,-1.23918376891,layer=self.layer)
        
        
        #Path of the bottom flat
        path4=gdspy.Path(1,(-16250,-47285.7))
        path4.segment(32500, "+x",layer=self.layer)
        
        #Path linking the left flat to the bottom flat
        path5=gdspy.Path(1,(-50000, 0))
        path5.arc(50000, np.pi,np.pi+1.058796649865,layer=self.layer)
        path5.rotate(0.1809871528,center=(0,0),)
        
        
        
        #Add the four rectangle
        rec1=gdspy.Rectangle((-10,-10), (10,10),layer=self.RectangleLayer)
        
        self.cellRect.add(rec1)
    
        
        
        self.cell.add([path1,path2,path3,path4,path5])
        self.cell.add(gdspy.CellReference(self.cellRect,origin=(0,50000)))
        self.cell.add(gdspy.CellReference(self.cellRect,origin=(0,-50000)))
        self.cell.add(gdspy.CellReference(self.cellRect,origin=(50000,0)))
        self.cell.add(gdspy.CellReference(self.cellRect,origin=(-50000,0)))
           
        
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)