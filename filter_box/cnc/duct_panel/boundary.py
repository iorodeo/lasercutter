from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 150.0
fileName = 'duct_panel.dxf'
depth = 0.51
startZ = 0.0
safeZ = 0.5
maxCutDepth = 0.15
toolDiam = 0.5 
direction = 'ccw'
startDwell = 1.0
startCond = 'minX'

ringPocketThickness = 1.0
ringPocketDepth = 0.1

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))


# ring pocket
param = {
        'fileName'       : fileName,
        'layers'         : ['ring_pocket'],
        'depth'          : ringPocketDepth,
        'thickness'      : ringPocketThickness,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : 0.6,
        'overlapFinish'  : 0.6,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
pocket = cnc_dxf.DxfCircPocket(param)
prog.add(pocket)

# inner boundary + duct hole
innerParam = {
        'fileName'     : fileName,
        'layers'       : ['duct_hole', 'inner_boundary'],
        'depth'        : depth,
        'startZ'       : startZ,
        'safeZ'        : safeZ,
        'toolDiam'     : toolDiam,
        'cutterComp'   : 'inside',
        'direction'    : direction,
        'maxCutDepth'  : maxCutDepth,
        'startDwell'   : startDwell,
        }
innerBoundary =cnc_dxf.DxfCircBoundary(innerParam)
prog.add(innerBoundary)

# outer boundary circles
outerCircParam = {
        'fileName'     : fileName,
        'layers'       : ['outer_boundary_circ'],
        'depth'        : depth,
        'startZ'       : startZ,
        'safeZ'        : safeZ,
        'toolDiam'     : toolDiam,
        'cutterComp'   : 'outside',
        'direction'    : direction,
        'maxCutDepth'  : maxCutDepth,
        'startDwell'   : startDwell,
        }
outerCircBoundary =cnc_dxf.DxfCircBoundary(outerCircParam)
prog.add(outerCircBoundary)

# outer boundary
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
