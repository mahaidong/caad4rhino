#coding=utf-8
'''
create on 2018.12.27
@author mahaidong
'''
import System
import os
import platform
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import caad.config as config
import urllib2

################lineType####################
#adding a lineType to document
def addLineType(lineTypeName):
    lineType = Rhino.DocObjects.Linetype()
    lineType.Default()
    lineType.Name = lineTypeName
    sc.doc.Linetypes.Add(lineType)

#editing a lineType by name
def editLineTypePattern(lineTypeName, pattern):
    lineType = sc.doc.Linetypes.FindName(lineTypeName)
    for index, segment in enumerate(pattern):
        if index%2 == 0 : lineType.AppendSegment(segment, False)
        else: lineType.AppendSegment(segment, True)
    lineType.RemoveSegment(0)
    lineType.CommitChanges()

################layer#####################
def initCaadLayer(name):
    caadLayer = Rhino.DocObjects.Layer()
    caadLayer.Name = name

    if name == "Axis":
        caadLayer.Color = System.Drawing.Color.Red
        lineType = sc.doc.Linetypes.FindName("Center")
        caadLayer.LinetypeIndex = lineType.Index  
    elif name == "Wall" :
        caadLayer.Color = System.Drawing.Color.Blue
        lineType = sc.doc.Linetypes.FindName("Continuous")
        caadLayer.LinetypeIndex = lineType.Index  
    elif name == "Opening" :
        caadLayer.Color = System.Drawing.Color.Green
        lineType = sc.doc.Linetypes.FindName("Continuous")
        caadLayer.LinetypeIndex = lineType.Index  
    elif name == "Dim":
        caadLayer.Color = System.Drawing.Color.Cyan
        lineType = sc.doc.Linetypes.FindName("Continuous")
        caadLayer.LinetypeIndex = lineType.Index  

    return sc.doc.Layers.Add(caadLayer)


################block####################
def initWindowBlock():
    if not rs.IsLayer("Opening"): 
        initCaadLayer("Opening")
    oldLayer = rs.CurrentLayer("Opening"); 
    line0 = rs.AddLine( (0.0, 0.0, 0.0), (1000.0, 0.0, 0.0) )
    line1 = rs.AddLine( (0.0, 50.0, 0.0), (1000.0, 50.0, 0.0) )
    line2 = rs.AddLine( (0.0, 100.0, 0.0), (1000.0, 100.0, 0.0) )
    block = rs.AddBlock((line0,line1,line2), (500,50,0), "window", True)
    rs.CurrentLayer(oldLayer); 

def initDoorBlock():
    if not rs.IsLayer("Opening"): 
        initCaadLayer("Opening")
    oldLayer = rs.CurrentLayer("Opening"); 
    line = rs.AddLine( (0.0, 0.0, 0.0), (0.0, 1000.0, 0.0) )
    arc = rs.AddArcPtTanPt( (1000,0,0), (0,1,0), (0,1000,0))
    block = rs.AddBlock((line,arc), (500,0,0), "door", True)
    rs.CurrentLayer(oldLayer); 

#################web######################
# Multithreaded Python
# https://stevebaer.wordpress.com/2011/06/01/multithreaded-python/
# https://realpython.com/intro-to-python-threading/

# url = "https://jsonplaceholder.typicode.com/posts/1"
def getContentFromUrl(url):
    response = urllib2.urlopen(url)
    # print response.read()
    lines = response.readlines()
    response.close() 
    return lines

# open a url
def openUrl(url):
    platformSystem = platform.system()
    if platformSystem == "Darwin":
        os.system("open \"\" " + url)
    elif platformSystem == "Windows":
        os.system("start \"\" " + url)



