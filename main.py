import sys
import bpy # type: ignore
import math
sys.path.append('/Users/lnewman/Documents/Blender/python/')
from cube import Cube, makeWindow

# sel = bpy.context.selected_objects
# act = bpy.context.active_object
# bpy.context.view_layer.objects.active = object #sets the obj accessible to bpy.ops
# window = makeWindow(dimensions=(10, 15), count=4, rows=2, thickness=0.4)

x, y, z = 4, 2, 2
cube1 = Cube('Rectangle 1', (x, y, z), (0, 0, 0))
cube1.move((0, 0, 0))
# cube1.loopCut(4, 0, 0)
print(f'Cube 1: {cube1}')

cube2 = Cube('Rectangle 2', (x, y, z), (0, 0, 0))
cube2.move((6, 0, 0))
cube2.rotate((0.0, 0.0, math.radians(90.0)))
# cube2.loopCut(4, 0, 1)
print(f'Cube 2: {cube2}')

cube1 = Cube('Rectangle 1')
cube1.createIntersection('Rectangle 2')
cube2.delete()