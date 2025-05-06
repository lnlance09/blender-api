import bpy # type: ignore
import bmesh # type: ignore
import mathutils as math # type: ignore
from mathutils import Euler, Vector, Matrix # type: ignore

def assignMaterial(obj, material):
    obj.data.materials.append(material)
    obj.active_material_index = len(obj.data.materials) - 1

def createCube(name, size, location):
    bpy.ops.mesh.primitive_cube_add(location=location)
    bpy.ops.transform.resize(value=size)
    cube = bpy.context.active_object
    cube.name = name
    cube.data.name = name
    return cube

def createIntersection(objName, intObjName):
    object = bpy.data.objects.get(objName)
    if object is None:
        print(f'Error: {object} not found.')
        exit()

    intObj = bpy.data.objects.get(intObjName)
    if intObj is None:
        print(f'Error: {intObjName} not found.')
        exit()
        
    modifier = object.modifiers.new(name='Boolean Mod 1', type='BOOLEAN')
    modifier.object = intObj
    modifier.operation = 'DIFFERENCE' # Set the operation type (e.g., 'DIFFERENCE', 'UNION', 'INTERSECT')
    modifier.solver = 'EXACT' # Optionally, set the solver (e.g., 'EXACT', 'FAST')
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.context.view_layer.objects.active = bpy.context.active_object

def loopCut(obj, num, smoothness):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = obj

    override = bpy.context.copy()
    override['area'] = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    override['region'] = next(region for region in override['area'].regions if region.type == 'WINDOW')
    override['space_data'] = override['area'].spaces.active

    bpy.ops.mesh.loopcut_slide(
        override,
        MESH_OT_loopcut_slide={
            'number_cuts': num,  # Number of cuts to make
            'smoothness': smoothness, # Smoothness factor
            'falloff': 'SMOOTH' # Falloff type
        },
        TRANSFORM_OT_edge_slide={
            'value': 0.5, # Slide amount (0.0 to 1.0)
            'mirror': False,
            'snap': False,
            'snap_target': 'CLOSEST',
            'snap_point': (0, 0, 0),
            'correct_uvs': True,
            'release_confirm': False
        }
    )
    bpy.ops.object.mode_set(mode='OBJECT')

'''
def bMeshLoopCut(bm, face_list, direction_axis, center='auto'):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))

    for f in bm.faces:
        f.select = False

    bm.faces.ensure_lookup_table()

    for f in face_list:
        bm.faces[f].select = True

    edges = [e for e in bm.edges if e.select == True]
    faces = [f for f in bm.faces if f.select == True]

    if center == 'auto':    
        weights = [f.calc_area() for f in faces]
        weighted_centres = [f.calc_area() * f.calc_center_median() for f in faces]
        cutting_point = sum(weighted_centres, math.Vector()) / sum(weights)
    else:
        cutting_point = bpy.context.scene.cursor.location

    geom = []
    geom.extend(edges)
    geom.extend(faces) 
    result = bmesh.ops.bisect_plane(bm, dist=0.01, geom=geom, plane_co=cutting_point, plane_no=direction_axis)
'''

def objDimensions(obj):
    return obj.dimensions

def objCopy(obj, data=True, actions=True, collection=None):
    objCopy = obj.copy()

    if data:
        objCopy.data = objCopy.data.copy()

    if actions and objCopy.animation_data:
        objCopy.animation_data.action = objCopy.animation_data.action.copy()

    collection.objects.link(objCopy)
    return objCopy

def objMove(obj, location):
    obj.location = Vector(location)

def objRotate(obj, location):
    obj.rotation_euler = Euler(location, 'XYZ')

def objUnlink(collection, obj):
    bpy.data.collections[collection].objects.unlink(obj)

def setOriginPoint(obj, location):
    if obj is None:
        print('No object selected. Cannot set origin point.')
        exit()

    bpy.ops.object.mode_set(mode='OBJECT')
    savedLocation = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = savedLocation

# Custom functions
def makeWindow(dimensions, count, rows, thickness):
    width = dimensions(0)
    height = dimensions(1)
    window = createCube(name='Window', size=(0.2, width, height), location=(1, width, height))
    panelW = (width / count) - thickness
    panelH = height - thickness    

    if rows == 1:
        for i in range(count):
            inc = (i * 2) + 1
            print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            createCube(name='Window Panel', size=(0.2, panelW, panelH), location=(1, x, y))
    if rows == 2:
        for i in range(count):
            inc = (i * 2) + 1
            print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            createCube(name='Window Panel', size=(0.2, panelW, panelH), location=(1, x, y))

    return window