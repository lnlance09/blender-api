import bpy # type: ignore
import bmesh # type: ignore
from cube import Cube
from utils import addArrayMod

def makeWindow(dimensions, count, rows, thickness):
    width = dimensions(0)
    height = dimensions(1)
    window = Cube("Window", (0.2, width, height), (1, width, height))
    panelW = (width / count) - thickness
    panelH = height - thickness    

    if rows == 1:
        for i in range(count):
            inc = (i * 2) + 1
            # print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            Cube("Window Panel", (0.2, panelW, panelH), (1, x, y))
    if rows == 2:
        for i in range(count):
            inc = (i * 2) + 1
            # print(f'i: {i}, inc: {inc}')
            x = (panelW + thickness) * inc
            y = (panelH + thickness)
            Cube("Window Panel", (0.2, panelW, panelH), (1, x, y))
    return window

def makePictureFrame(width, offset, height, thickness):
    Cube("Cube1", dimensions=(1, 1, 1))
    obj = bpy.data.objects.get("Cube1")
    obj = bpy.context.edit_object
    bpy.ops.object.mode_set(mode="EDIT")

    # Front face bottom
    obj.data.vertices[0].co[0] = 0.0
    obj.data.vertices[0].co[1] = 0.0
    obj.data.vertices[0].co[2] = 0.0

    obj.data.vertices[4].co[0] = width
    obj.data.vertices[4].co[1] = 0.0
    obj.data.vertices[4].co[2] = 0.0

    # Front face top
    obj.data.vertices[1].co = (0.0 - offset, 0.0, height)
    obj.data.vertices[5].co = (width + offset, 0.0, height)

    # Bottom face bottom
    obj.data.vertices[2].co = (0.0, thickness, 0.0)
    obj.data.vertices[6].co = (width, thickness, 0.0)

    # Bottom face top
    obj.data.vertices[3].co = (0.0 - offset, thickness, height)
    obj.data.vertices[7].co = (width + offset, thickness, height)

    # mesh.update()
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode="OBJECT")

def makeHardWoodFloor(width, height):
    floorX = 3
    floorY = 0.5
    woodHeight = 0.1
    i = 0
    while i < height:
        key = i + 1
        x = 0 if key != int(key) else 0 - (floorX / 2)
        y = i
        z = 0 - woodHeight
        length = (width / floorX) - 1
        if key == int(key):
            length = length + 1 

        floor = Cube(f"HardWood Floor-{key}", dimensions=(floorX, floorY, woodHeight))
        floor.setCursorToBottom()
        floor.move((x, y, z))
        floor.assignMaterial("Toon_BROWN (Dark)")
        addArrayMod(obj=floor.cube, length=length, offset=(1, 0, 0))
        # floor.cube.rotation_euler.z = math.radians(270)
        i += floorY

def makeTiledFloor(roomWidth, roomHeight, wallWidth):
    floorX = 1
    floorY = 1
    modX = roomWidth - floorX

    for i in range(roomHeight):
        key = i + 1
        floor1 = Cube(f"Floor1-{key}", dimensions=(floorX, floorY, wallWidth))
        floor1.setCursorToBottom()
        floor1.move((0, roomHeight - key, 0 - wallWidth))
        material1 = "Toon_BLACK" if key % 2 == 0 else "Toon_WHITE (01)"
        floor1.assignMaterial(material1)
        addArrayMod(obj=floor1.cube, length=modX, offset=(2, 0, 0))

        floor2 = Cube(f"Floor2-{key}", dimensions=(floorX, floorY, wallWidth))
        floor2.setCursorToBottom()
        floor2.move((floorX, roomHeight - key, 0 - wallWidth))
        material2 = "Toon_WHITE (01)" if key % 2 == 0 else "Toon_BLACK"
        floor2.assignMaterial(material2)
        addArrayMod(obj=floor2.cube, length=modX - 1, offset=(2, 0, 0))

def makeRoom(wallWidth, wallHeight, roomWidth, roomHeight):
    leftWall = Cube("Left Wall", dimensions=(wallWidth, roomHeight, wallHeight))
    leftWall.setCursorToBottom()
    leftWall.move((0, 0, 0))
    leftWall.assignMaterial("Toon_WHITE (Cream)")

    backWall = Cube('Back Wall', dimensions=(roomWidth, wallWidth, wallHeight))
    backWall.setCursorToBottom()
    backWall.move((0, roomHeight, 0))
    backWall.assignMaterial("Toon_WHITE (Cream)")

    rightWall = Cube('Right Wall', dimensions=(wallWidth, roomHeight, wallHeight))
    rightWall.setCursorToBottom()
    rightWall.move((roomWidth - wallWidth, 0, 0))
    rightWall.assignMaterial("Toon_WHITE (Cream)")

    # makeTiledFloor(roomWidth, roomHeight, wallWidth)
    makeHardWoodFloor(roomWidth, roomHeight)