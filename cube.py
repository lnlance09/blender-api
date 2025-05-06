import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
from mathutils import Euler, Vector, Matrix # type: ignore

class Cube:
    def __init__(self, name, size=None, location=None):
        obj = bpy.data.objects.get(name)
        if obj == None:
            self.name = name
            self.size = size
            self.location = location
            self.cube = self.create(name, size, location)
            self.setOriginPoint(tuple([-x for x in size]))
        else:
            self.name = obj.name
            self.size = obj.dimensions
            self.location = obj.location
            self.cube = obj
    
    def assignMaterial(self, material):
        self.cube.data.materials.append(material)
        self.cube.active_material_index = len(self.cube.data.materials) - 1

    def create(self, name, size, location):
        bpy.ops.mesh.primitive_cube_add(location=location)
        bpy.ops.transform.resize(value=size)
        cube = bpy.context.active_object
        cube.name = name
        cube.data.name = name
        return cube

    def createIntersection(self, obj):
        obj = bpy.data.objects.get(obj)
        if obj is None:
            print(f'Error: {obj} not found.')
            exit()
            
        modifier = self.cube.modifiers.new(name='Boolean Mod 1', type='BOOLEAN')
        modifier.object = obj
        modifier.operation = 'DIFFERENCE' # Set the operation type (e.g., 'DIFFERENCE', 'UNION', 'INTERSECT')
        modifier.solver = 'EXACT' # Optionally, set the solver (e.g., 'EXACT', 'FAST')
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.object.modifier_apply(modifier=modifier.name)

    def copy(self, data=True, actions=True, collection=None):
        objCopy = self.cube.copy()
        if data:
            objCopy.data = objCopy.data.copy()
        if actions and objCopy.animation_data:
            objCopy.animation_data.action = objCopy.animation_data.action.copy()
        collection.objects.link(objCopy)
        return objCopy
    
    def delete(self):
        print(f'Instance {self.name} destroyed')
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.object.delete()
    
    def dimensions(self):
        return self.cube.dimensions

    def loopCut(self, num, smoothness, axis):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.view_layer.objects.active = self.cube
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut = {
                'number_cuts': num,  # Number of cuts to make
                'smoothness': smoothness, # Smoothness factor
                'falloff': 'SMOOTH', # Falloff type
                'edge_index': axis, # 0 = x axis, 1 = y axis, 2 = z axis
                'object_index': 0,
                'mesh_select_mode_init': (True, False, False)
            },
            TRANSFORM_OT_edge_slide = {
                'value': 0, # Slide amount (0.0 to 1.0)
                'mirror': False,
                'snap': False,
                'snap_target': 'CLOSEST',
                'snap_point': (0, 0, 0),
                'correct_uv': False,
                'release_confirm': False,
                'use_accurate': False
            }
        )
        bpy.ops.object.mode_set(mode='OBJECT')

    def move(self, location):
        self.cube.location = Vector(location)

    def rotate(self, location):
        self.cube.rotation_euler = Euler(location, 'XYZ')

    def setOriginPoint(self, location):
        savedLocation = bpy.context.scene.cursor.location.copy()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.cursor.location = location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor.location = savedLocation

    def unlink(self, collection):
        bpy.data.collections[collection].objects.unlink(self.cube)


def makeWindow(dimensions, count, rows, thickness):
    width = dimensions(0)
    height = dimensions(1)
    window = Cube('Window', (0.2, width, height), (1, width, height))
    panelW = (width / count) - thickness
    panelH = height - thickness    

    if rows == 1:
        for i in range(count):
            inc = (i * 2) + 1
            # print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            Cube('Window Panel', (0.2, panelW, panelH), (1, x, y))
    if rows == 2:
        for i in range(count):
            inc = (i * 2) + 1
            # print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            Cube('Window Panel', (0.2, panelW, panelH), (1, x, y))

    return window