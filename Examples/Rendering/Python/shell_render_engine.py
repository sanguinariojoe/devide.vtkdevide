# $Id$
# example to test shell renderer (*shudder*)

import vtk
from vtk import *
from vtkdevide import *
import time

def bench(camera, rwi):
    initial_time = time.clock()
    for i in range(36):
        camera.Azimuth(10)
        rwi.Render()
    
    end_time = time.clock()

    print "FPS == %f" % (36 / (end_time - initial_time))
    
def bench2(camera, rwi):
    initial_time = time.clock()

    numberOfRenders = 10 * (36 + 1)
    
    for i in range(10):
        for j in range(36):
            camera.Azimuth(10)
            rwi.Render()
        
        camera.Elevation(36 * i)
        rwi.Render()
            
            
    
    end_time = time.clock()

    print "FPS == %f" % (numberOfRenders / (end_time - initial_time))
    
    
textActor = vtk.vtkTextActor()

def ce_cb(obj, evt_name):
    if obj.GetKeyCode() == 'm':
        crm = splatmapper.GetRenderMode()
	crm = crm + 1
	if crm > 2:
	    crm = 0
        splatmapper.SetRenderMode(crm)
        print "rendermode switched to %d" % (crm)

    if obj.GetKeyCode() in ['0', '1', '2', '4']:
#         com = splatmapper.GetPerspectiveOrderingMode()
# 	com = com + 1
# 	if com > 2:
# 	    com = 0

        com = int(obj.GetKeyCode())
        if com == 4:
            com = 3
            
        splatmapper.SetPerspectiveOrderingMode(com)
        print "ordering mode switched to %d" % (com)
        
        if com == 0:
            textActor.SetInput("PBTF")
        elif com == 1:
            textActor.SetInput("IP-PBTF")
        elif com == 2:
            textActor.SetInput("Traditional BTF")
        else:
            textActor.SetInput("New-style IP-PBTF")

        #textActor.GetPosition2Coordinate().SetValue(1, 1)
        textActor.SetDisplayPosition(0, 140)
        rwi.Render()
        time.sleep(1.2)
        textActor.SetDisplayPosition(0, 10)

    elif obj.GetKeyCode() == '\'':
        cur = splatmapper.GetEllipsoidDiameter()
        splatmapper.SetEllipsoidDiameter(cur - 0.1)
        print "EllipsoidDiameter == %s" % str(cur - 0.1)
    elif obj.GetKeyCode() == ',':
        cur = splatmapper.GetEllipsoidDiameter()
        splatmapper.SetEllipsoidDiameter(cur + 0.1)
        print "EllipsoidDiameter == %s" % str(cur + 0.1)
        
    elif obj.GetKeyCode() == 'd':
        cur = splatmapper.GetGaussianRadialExtent()
        splatmapper.SetGaussianRadialExtent(cur - 0.1)
        print "GaussianRadialExtent == %s" % str(cur - 0.1)
    elif obj.GetKeyCode() == 'h':
        cur = splatmapper.GetGaussianRadialExtent()
        splatmapper.SetGaussianRadialExtent(cur + 0.1)
        print "GaussianRadialExtent == %s" % str(cur + 0.1)
        
    elif obj.GetKeyCode() == 't':
        cur = splatmapper.GetGaussianSigma()
        splatmapper.SetGaussianSigma(cur - 0.1)
        print "GaussianSigma == %s" % str(cur - 0.1)
    elif obj.GetKeyCode() == 'n':
        cur = splatmapper.GetGaussianSigma()
        splatmapper.SetGaussianSigma(cur + 0.1)
        print "GaussianSigma == %s" % str(cur + 0.1)
        
    elif obj.GetKeyCode() == 'b':
        bench2(ren.GetActiveCamera(), rwi)
        
    rwi.Render()
        
        
reader = vtkImageReader()
reader.SetHeaderSize(0)
reader.SetFileDimensionality(3)
reader.SetFileName("engine.raw")
reader.SetDataScalarType(3)
reader.SetDataExtent(0,255,0,255,0,127)
reader.SetDataSpacing(1,1,1)

otf = vtkPiecewiseFunction()
otf.AddPoint(0.0, 0.0)
otf.AddPoint(130, 0.0)
otf.AddPoint(130.1, 1)
otf.AddPoint(180.0, 1)
otf.AddPoint(180.1, 1)
otf.AddPoint(255.0, 1)

ctf = vtkColorTransferFunction()
ctf.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
ctf.AddRGBPoint(130, 0.0, 0.0, 0.0)
ctf.AddRGBPoint(130.1, 0.80, 0.80, 0.80)
ctf.AddRGBPoint(180.0, 0.80, 0.80, 0.80)
ctf.AddRGBPoint(180.1, 0.91, 0.61, 0.10)
ctf.AddRGBPoint(255.0, 0.91, 0.61, 0.10)

#se = vtkShellExtractor()
#se.SetInput(hdfr.GetOutput())
#se.SetOpacityTF(otf)
#se.SetOmegaL(0.8)
#se.SetOmegaH(0.99)

#se.Update()

splatmapper = vtkOpenGLVolumeShellSplatMapper()
splatmapper.SetOmegaL(0.1)
splatmapper.SetOmegaH(0.2)
splatmapper.SetInput(reader.GetOutput())
splatmapper.SetRenderMode(0)
# this should be PBTF
splatmapper.SetPerspectiveOrderingMode(0)

vprop = vtkVolumeProperty()
vprop.SetScalarOpacity(otf)
vprop.SetColor(ctf);
vprop.ShadeOn()
vprop.SetAmbient(0.1)
vprop.SetDiffuse(0.7)
vprop.SetSpecular(0.4)
vprop.SetSpecularPower(40)

volume = vtkVolume()
volume.SetProperty(vprop)
volume.SetMapper(splatmapper)

ren = vtkRenderer()
ren.SetBackground(0.5, 0.5, 0.5)
ren.AddVolume(volume)
#ren.GetActiveCamera().ParallelProjectionOn()

cubeAxesActor2d = vtk.vtkCubeAxesActor2D()
cubeAxesActor2d.SetFlyModeToOuterEdges()
ren.AddActor(cubeAxesActor2d)
cubeAxesActor2d.VisibilityOff() # FIXME: you can switch it on here
reader.Update()
cubeAxesActor2d.SetBounds(reader.GetOutput().GetBounds())
cubeAxesActor2d.SetCamera(ren.GetActiveCamera())

# Create a scaled text actor. 

textActor.ScaledTextOn()
textActor.SetDisplayPosition(0, 10)
textActor.SetInput("PBTF")

# Set coordinates to match the old vtkScaledTextActor default value
textActor.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
textActor.GetPosition2Coordinate().SetValue(1, 0.1)

tprop = textActor.GetTextProperty()
tprop.SetFontSize(18)
tprop.SetFontFamilyToArial()
tprop.SetJustificationToCentered()
tprop.BoldOn()
#tprop.ItalicOn()
tprop.ShadowOn()
tprop.SetColor(1, 0, 0)

# FIXME: switch text actor on here
ren.AddActor(textActor)
#### end of text




renwin = vtkRenderWindow()
renwin.SetSize(512,512)
renwin.AddRenderer(ren)

rwi = vtkRenderWindowInteractor()
rwi.SetRenderWindow(renwin)

rwi.AddObserver('CharEvent', ce_cb)

#rwi.LightFollowCameraOn();
rwi.Initialize()
rwi.Start()

