import bpy
import json
import random
import os

path = r"C:\Users\smith\OneDrive\Documents\Blender\files"

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
#bpy.ops.outliner.item_activate(deselect_all=True)
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -0.5, -1.2), rotation=(0, 3.14, 3.14), scale=(1, 1, 1))
camera = bpy.context.active_object
camera.data.lens = 25
bpy.context.scene.camera = camera
 

objs = {
    "Car": [], 
    "BaseMesh_Man_Simple": [],
    "Traffic_signal1": [],
    "truck": [],
    "absperrhut": [],
    "roadbike 2.0.1": [],
    "fire hydrant": [],
    "stop sign": [],
    "bird": [],
    "refrigerator": [],
    "bench": [],
    "train": [],
    "umbrella": []
}


def create_obj(tag,times,blend_file_path,ret):
        
    for i in range(times):
        with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
            print("TO data",data_to.meshes)
            print("From data",data_from)
            data_to.objects = [tag]

        print(data_to.objects)
        obj = data_to.objects[0]
        print("added object",obj.name)
        bpy.context.collection.objects.link(obj)
        if tag == "Car":
            obj.scale = (0.02,0.02,0.02)
            obj.rotation_euler = (-1.57,0.0,3.14)
        if tag == "Traffic_signal1":
            obj.scale = (0.8,0.8,0.8)
            obj.rotation_euler = (0,1.57,0)
        if ret:
            return obj
        objs[tag].append(obj)
    
def delete_obj(tag,times):
    for i in range(times):
        temp = objs[tag].pop()
#        bpy.context.collection.objects.unlink(temp)
        bpy.data.objects.remove(temp)


def update_location(obj):
    obj.location = (-100,-100,-100)
    obj.keyframe_insert(data_path="location",index=-1,frame=frame_nos+1)
    pass


def make_invisible():
    bpy.ops.object.select_all(action='SELECT')

    # Set selected objects to invisible
    for obj in bpy.context.selected_objects:
        obj.hide_set(True)
        obj.hide_render = True
        
        
dict = {
    "Car": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\Vehicles\SedanAndHatchback.blend",
    "BashMesh_Man_Simp": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\Pedestrain.blend",
    "Traffic_signal1": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\TrafficSignal.blend",
    "truck": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\Vehicles\PickupTruck.blend",
    "absperrhut": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\TrafficConeAndCylinder.blend",
    "roadbike 2.0.1": r"C:\Users\smith\OneDrive\Documents\Blender\P3Data\P3Data\Assets\Vehicles\Bicycle.blend",
    "fire hydrant":"",
    "stop sign": "",
    "bird": "",
    "refrigerator": "",
    "bench": "",
    "train": "",
    "umbrella": ""
    }

json_file_path = r"C:\Users\smith\OneDrive\Documents\Blender\\location_seq9_1.json"

with open(json_file_path, 'r') as file:
    object_data = json.load(file)
datas = object_data['data'][0]
exit_loop = False
i = 0
for key,value in datas.items():
    if int(key) == 1:
        bpy.context.scene.frame_set(int(key))
        frame_nos = int(key)
    else:
        bpy.context.scene.frame_set(int(key)*10)
        frame_nos = int(key)* 10
    # Clear the scene and remove all objects
#    bpy.ops.object.select_all(action='DESELECT')
    
    details = value
    
    if exit_loop:
        break
    # make_invisible()
#    bpy.ops.object.select_all(action='DESELECT')
#    bpy.ops.object.select_by_type(type='MESH')
#    bpy.ops.object.delete()
#    bpy.ops.object.select_all(action='SELECT')
#    bpy.ops.object.delete()
#    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -0.5, 1.2), rotation=(0, 3.14, 3.14), scale=(1, 1, 1))
#    camera = bpy.context.active_object
#    camera.data.lens = 25
    
    for tag,poses in details.items():
        blend_file_path = dict[tag]
        if tag == "truck":
            tag = "PickupTruck"
        if tag == "BashMesh_Man_Simp":
            tag = "BaseMesh_Man_Simple"

        if blend_file_path == "":
            continue
        if tag == 'Car':
            print("Lengths = ", len(poses),len(objs[tag]))
            if len(poses) > len(objs[tag]):
                create_obj(tag=tag,times=len(poses)-len(objs[tag]),blend_file_path=blend_file_path,ret=False)
            elif len(poses) < len(objs[tag]):
                delete_obj(tag=tag,times=len(objs[tag])- len(poses))

            if exit_loop:
                break
            

            for pose,obj in zip(poses,objs[tag]):
                i+=1
                loc = pose[0]
                if exit_loop:
                    break
                print("added object",obj.name)
                print(loc)
                obj.location = ((loc[0],loc[1],loc[2]))
                obj.keyframe_insert(data_path="location",index=-1,frame=frame_nos)
                

        else:
            for pose in poses:
                obj = create_obj(tag=tag,times=1,blend_file_path=blend_file_path,ret=True)
                loc = pose[0]
                print("added object",obj.name)
                print(loc)
                obj.location = ((loc[0],loc[1],loc[2]))
                obj.keyframe_insert(data_path="location",index=-1,frame=frame_nos)
                bpy.context.view_layer.objects.active = obj
                temp = bpy.context.active_object
                temp.hide_set(True)
                obj.keyframe_insert(data_path="hide",index=-1,frame=frame_nos+1)
                obj.hide_render = True
                obj.keyframe_insert(data_path="hide_render", index=-1)
#                update_location(obj=obj)
#                bpy.data.objects.remove(obj)
#                bpy.context.collection.objects.unlink(obj)
                

                if i > 100:
                    exit_loop = True

    
#bpy.context.scene.render.filepath = os.path.join(path,"frame%04d" %(bpy.data.scenes[0].frame_current))
#bpy.ops.render.render(write_still=True)
bpy.context.scene.frame_end = frame_nos
#bpy.context.scene.render.filepath = r"C:\Users\smith\OneDrive\Documents\Blender\render.mp4"
#bpy.context.scene.render.image_settings.file_format = "FFMPEG"
#bpy.ops.render.render(animation=True)
# with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):