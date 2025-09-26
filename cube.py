import sys
import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
sys.path.append("/Users/lnewman/Documents/Blender/python/")

class Cube:
    def __init__(self, name, size=1, dimensions=(0, 0, 0), location=(0, 0, 0)):
        obj = bpy.data.objects.get(name)
        if obj is None:
            self.name = name
            self.size = size
            self.dimensions = dimensions
            self.cube = self.create(name, size=size, location=location, dimensions=dimensions)
            self.cube.location = mathutils.Vector(location)
        else:
            self.name = obj.name
            self.dimensions = obj.dimensions
            self.location = obj.location
            self.cube = obj

    def create(self, name, size, location, dimensions):
        bpy.ops.mesh.primitive_cube_add(
            size=size,
            location=location
        )
        cube = bpy.context.active_object
        cube.name = name
        cube.data.name = name
        cube.dimensions = dimensions
        return cube
    
    def move(self, location):
        self.cube.location = mathutils.Vector(location)

    def rotate(self, location):
        self.cube.rotation_euler = mathutils.Euler(location, "XYZ")

    def copy(self, data=True, actions=True, collection=None):
        objCopy = self.cube.copy()
        if data:
            objCopy.data = objCopy.data.copy()
        if actions and objCopy.animation_data:
            objCopy.animation_data.action = objCopy.animation_data.action.copy()
        collection.objects.link(objCopy)
        return objCopy
    
    def delete(self):
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.object.delete()
        print(f"Cube {self.name} deleted")
        
    def unlink(self, collection):
        bpy.data.collections[collection].objects.unlink(self.cube)
    
    def dimensions(self):
        return self.cube.dimensions

    def assignMaterial(self, materialName):
        obj = bpy.data.objects.get(self.cube.name)
        material = bpy.data.materials.get(materialName)
        obj.data.materials.append(material)
        # self.cube.active_material_index = len(self.cube.data.materials) - 1

    def loopCut(self, num, smoothness, axis):
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut = {
                "number_cuts": num,  # Number of cuts to make
                "smoothness": smoothness, # Smoothness factor
                "falloff": "SMOOTH", # Falloff type
                "edge_index": axis, # 0 = x axis, 1 = y axis, 2 = z axis
                "object_index": 0,
                "mesh_select_mode_init": (True, False, False)
            },
            TRANSFORM_OT_edge_slide = {
                "value": 0, # Slide amount (0.0 to 1.0)
                "mirror": False,
                "snap": False,
                "snap_target": "CLOSEST",
                "snap_point": (0, 0, 0),
                "correct_uv": False,
                "release_confirm": False,
                "use_accurate": False
            }
        )
        bpy.ops.object.mode_set(mode="OBJECT")
        
    def createIntersection(self, obj):
        obj = bpy.data.objects.get(obj)
        if obj is None:
            print(f"Error: {obj} not found.")
            exit()
        modifier = self.cube.modifiers.new(name="Boolean Mod 1", type="BOOLEAN")
        modifier.object = obj
        modifier.operation = "DIFFERENCE" # Set the operation type (e.g., 'DIFFERENCE', 'UNION', 'INTERSECT')
        modifier.solver = "EXACT" # Optionally, set the solver (e.g., 'EXACT', 'FAST')
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    def setCursorToBottom(self):
        ctx = bpy.context
        if ctx.mode != "EDIT_MESH":
            bpy.ops.object.mode_set(mode="EDIT")

        obj = bpy.data.objects.get(self.cube.name)
        if obj is None:
            print(f"Error: {obj} not found.")
            exit()

        bm = bmesh.from_edit_mesh(obj.data)
        lowestX = float("inf")
        lowestY = float("inf")
        lowestZ = float("inf")
        lowestVertex = None

        for vert in bm.verts:
            if vert.co.x < lowestX:
                lowestX = vert.co.x
                lowestVertex = vert
            if vert.co.y < lowestY:
                lowestY = vert.co.y
                lowestVertex = vert
            if vert.co.z < lowestZ:
                lowestZ = vert.co.z
                lowestVertex = vert
        '''
        print(f'Lowest X: {lowestX}')
        print(f'Lowest Y: {lowestY}')
        print(f'Lowest Z: {lowestZ}')
        print(f'Lowest Vertex: {lowestVertex}')
        '''
        if lowestVertex:
            lowestVertexWorldLocation = obj.matrix_world @ lowestVertex.co
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.context.scene.cursor.location = lowestVertexWorldLocation
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            print(f"3D cursor set to the lowest vertex at: {lowestVertexWorldLocation}")
        else:
            print("No vertices found on the active object.")

        bpy.ops.object.mode_set(mode="OBJECT")