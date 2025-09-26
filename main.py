import bpy # type: ignore
import sys
sys.path.append("/Users/lnewman/Documents/Blender/python/")
import math
from pathlib import Path
from cube import Cube
from utils import appendFile, setCursorToDefault
from simpsonsObjs import allObjs

setCursorToDefault()

for obj in allObjs:
    appendFile(
        path=Path.home() / "Documents" / "Blender" / "NPR Master Pack" / "Assets",
        file="Blender NPR Master Pack_Individual Assets.blend",
        dataType="Mesh",
        dataName=obj
    )
    data = bpy.data.objects.get(obj)
    print(f"data: {data}")
    if data is not None:
        if data.cube is not None:
            x = data.cube.dimensions[0]
            y = data.cube.dimensions[1]
            z = data.cube.dimensions[2]
 
# makePictureFrame(width=10, offset=1, height=3, thickness=3)
# makeRoom(wallWidth=0.1, wallHeight=5, roomWidth=15, roomHeight=7)
# setCursorToDefault()

'''
x, y, z = 4, 0.1, 2
brick1 = Cube('Brick 47', (4.3, 2.5, 1.3))
# cube1 = Cube('Rectangle 1', (x, y, z), (0, 0, 0))
# setCursorToDefault()
'''

'''
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
'''