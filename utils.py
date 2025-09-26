import bpy # type: ignore
import math # type: ignore

def appendFile(path="", file="", dataType="Mesh", dataName=""):
    dataPath = f"{path / file}/{dataType}/{dataName}"
    bpy.ops.wm.append(
        filepath=dataPath,
        directory=f"{path / file}/{dataType}/",
        filename=dataName
    )

def addArrayMod(obj, count = None, length = None, offset = ()):
    arrayMod = obj.modifiers.new(name="ArrayMod", type="ARRAY")
    if count:
        arrayMod.count = count
    if length:
        arrayMod.fit_type = "FIT_LENGTH"
        arrayMod.fit_length = length
    arrayMod.relative_offset_displace[0] = offset[0] # x
    arrayMod.relative_offset_displace[1] = offset[1] # y
    arrayMod.relative_offset_displace[2] = offset[2] # z

def setCursorToDefault():
    bpy.context.scene.cursor.location = (0, 0, 0)

def changeMaterial(collectionName, materialName):
    collection = bpy.data.collections.get(collectionName)
    if not collection:
        return False
    targetMaterial = bpy.data.materials.get(materialName)
    if not targetMaterial:
        return False
    for obj in collection.objects:
        # obj.data.materials.clear()
        obj.data.materials.append(targetMaterial)

def changeRotation(collectionName, rotation):
    collection = bpy.data.collections.get(collectionName)
    if collection:
        rotationAngleZ = math.radians(rotation)
        for obj in collection.objects:
            obj.rotation_euler.z = rotationAngleZ
        print(f"Rotation applied to all objects in collection '{collectionName}'.")
    else:
        print(f"Collection '{collectionName}' not found.")

def deleteAll():
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()

def addCamera(location=(0.0, 0.0, 5.0), rotation=(0.0, 0.0, 5.0)):
    bpy.ops.object.camera_add(
        enter_editmode=False,
        align="WORLD",
        location=location,
        rotation=rotation
    )
    cameraObj = bpy.context.object
    bpy.context.scene.camera = cameraObj
    '''
    cameraData = cameraObj.data
    cameraData.type = 'PERSP'
    cameraData.lens = 50 # Lens focal length in mm
    cameraData.clip_start = 0.1 # Near clipping distance
    cameraData.clip_end = 100.0 # Far clipping distance
    '''

def generateImg(format="PNG", filename="//output_image.png", width=1920, height=1080):
    '''
    # Set camera position and rotation
    cameraData = bpy.data.cameras.new(name="Camera")
    myCamera = bpy.data.objects.new("Camera", cameraData)
    bpy.context.scene.collection.objects.link(myCamera)
    myCamera.location = (5, -5, 5)
    myCamera.rotation_euler = (0.785, 0, 0.785) # Roughly looking at the cube
    '''
    # bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.image_settings.file_format = format
    bpy.context.scene.render.filepath = filename # Saves in the same directory as the .blend file
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.ops.render.render(write_still=True)