from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 150.0
fileName = 'middle_center_in.dxf'
depth = 0.51
startZ = 0.0
safeZ = 0.5
maxCutDepth = 0.15
toolDiam = 0.5 
direction = 'ccw'
cutterComp = 'inside'
startDwell = 1.0
startCond = 'minX'

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

param = {
        'fileName'     : fileName,
        'layers'       : ['VENT_CUTOUT'], 
        'depth'        : depth,
        'startZ'       : startZ,
        'safeZ'        : safeZ,
        'toolDiam'     : toolDiam,
        'cutterComp'   : cutterComp,
        'direction'    : direction,
        'maxCutDepth'  : maxCutDepth,
        'startDwell'   : startDwell,
        }
boundary = cnc_dxf.DxfCircBoundary(param)
prog.add(boundary)


prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
