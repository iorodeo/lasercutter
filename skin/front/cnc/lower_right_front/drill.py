from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

feedrate = 50.0
fileName = 'lower_right_front_in.dxf'
stockThickness = 0.25
drillMargin = 0.125

startZ = 0.0
stopZ = -(stockThickness + drillMargin)
safeZ = 0.3
stepZ = 0.04
startDwell = 0.5

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

param = { 
        'fileName'    : fileName,
        'layers'      : ['6-32_TAP_HOLE'],
        'dxfTypes'    : ['CIRCLE'],
        'startZ'      : startZ,
        'stopZ'       : stopZ,
        'safeZ'       : safeZ,
        'stepZ'       : stepZ,
        'startDwell'  : startDwell,
        }
drill = cnc_dxf.DxfDrill(param)
prog.add(drill)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
