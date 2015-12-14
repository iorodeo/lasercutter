from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 150.0
fileName = 'insert_panels.dxf'
depth = 0.51
startZ = 0.0
safeZ = 0.5
maxCutDepth = 0.15
toolDiam = 0.5 
direction = 'ccw'
startDwell = 1.0
startCond = 'minX'

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

innerParam = {
        'fileName'    : fileName,
        'layers'      : ['inner_boundary'],
        'depth'       : depth,
        'startZ'      : startZ,
        'safeZ'       : safeZ,
        'toolDiam'    : toolDiam,
        'direction'   : direction,
        'cutterComp'  : 'inside',
        'maxCutDepth' : maxCutDepth,
        'startDwell'  : startDwell, 
        'startCond'   : startCond,
        }
innerBoundary = cnc_dxf.DxfBoundary(innerParam)
prog.add(innerBoundary)


outerParam = {
        'fileName'    : fileName,
        'layers'      : ['outer_boundary'],
        'depth'       : depth,
        'startZ'      : startZ,
        'safeZ'       : safeZ,
        'toolDiam'    : toolDiam,
        'direction'   : direction,
        'cutterComp'  : 'outside',
        'maxCutDepth' : maxCutDepth,
        'startDwell'  : startDwell, 
        'startCond'   : startCond,
        }
outerBoundary = cnc_dxf.DxfBoundary(outerParam)
prog.add(outerBoundary)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
