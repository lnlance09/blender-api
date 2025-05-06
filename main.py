import sys
import bpy # type: ignore
import bmesh # type: ignore
sys.path.append('/Users/lnewman/Documents/Blender/python/')
import functions as Blender

# window = Blender.makeWindow(dimensions=(10, 15), count=4, rows=2, thickness=0.4)
# Blender.setOriginPoint(obj=window)

cube1Name = 'Rectangle 1'
x, y, z = 4, 2, 2
cube1 = Blender.createCube(name=cube1Name, size=(x, y, z), location=(0, 0, 0))
Blender.setOriginPoint(obj=cube1, location=(-x, -y, -z))
Blender.objMove(obj=cube1, location=(-x, -y, 0))

# sel = bpy.context.selected_objects
# act = bpy.context.active_object
# bpy.context.view_layer.objects.active = object #sets the obj accessible to bpy.ops

# Blender.createIntersection(objName=cube1Name, intObjName='Sidewalk')

me = bpy.context.object.data
bm = bmesh.new() 
bm.from_mesh(me)
# Blender.bMeshLoopCut(bm, faceCut=([0]), [1, 0, 0])    
bm.to_mesh(me)
bm.free()
me.update()