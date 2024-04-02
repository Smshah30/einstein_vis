import bpy
import json
import random
import os


class Blender():
    def __init__(self) -> None:
        self.blend_file_path = r"C:\Users\smith\OneDrive\Documents\Blender\Everything.blend"
        self.main_objs = {}
        self.get_objects()
        print(self.main_objs)
        self.json_path = r"C:\Users\smith\OneDrive\Documents\Blender\\location_seq9_1.json"
        self.duplicates = {
            "Car": [], 
            "BaseMesh_Man_Simple": [],
            "Traffic_signal1": [],
            "truck": [],
            "absperrhut": [],
            "roadbike 2": [],
        }


    def create_duplicate(self,tag):
        obj = self.main_objs[tag]
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)
        return new_obj
    

    def update_location(self,unused,frame_num):
        for obj in unused:
            obj.location = (-100,-100,-100)
            obj.keyframe_insert(data_path="location",index=-1,frame=frame_num-19)

    def get_objects(self):
        with bpy.data.libraries.load(self.blend_file_path) as (data_from, data_to):
            data_to.objects = data_from.objects

        # Link the objects to the scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                temp = str(obj.name).split('.')[0]
                self.main_objs[temp] = obj

    def set_camera(self):
        # cam = self.main_objs['Camera']
        # bpy.context.view_layer.objects.active = cam
        # cam = bpy.context.active_object
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -0.5, -1.2), rotation=(0, 3.14, 3.14), scale=(1, 1, 1))
        cam = bpy.context.active_object
        # cam.location = (0, -0.5, -1.2)
        # cam.rotation_euler = (0, 3.14, 3.14)
        cam.data.lens = 25
        bpy.context.scene.camera = cam
    def rename(self,tag):
        if tag == "Car":
            tag = "Car.003"
        if tag == "Traffic_signal1":
            tag = "Traffic_signal1.003"
        if tag == "roadbike 2.0.1":
            tag = "roadbike 2.0.004"
        if tag == "BaseMesh_Man_Simple":
            tag = "BaseMesh_Man_Simple.003"
        if tag == "Truck":
            tag = "Truck.003"
        if tag == "absperrhut":
            tag = "absperrhut.003"
        
        return tag



    def run(self):
        with open(self.json_path,'r') as file:
            object_data = json.load(file)
        datas = object_data['data'][0]
        exit_loop = False
        i = 0
        for key,value in datas.items():
            if int(key) == 1:
                bpy.context.scene.frame_set(int(key))
                frame_nos = int(key)
            else:
                bpy.context.scene.frame_set(int(key)*20)
                frame_nos = int(key)* 20
            if exit_loop:
                break

            for tag,poses in value.items():
                if tag == "truck":
                    tag = "Truck"
                if tag == "BashMesh_Man_Simp":
                    tag = "BaseMesh_Man_Simple"
                if tag == "roadbike 2.0.1":
                    tag = "roadbike 2"
                if not tag in self.duplicates:
                    continue
                # tag = self.rename(tag=tag)
                if "Car" in tag:
                    print("Lengths = ", len(poses),len(self.duplicates[tag]))
                    diff = abs(len(poses)-len(self.duplicates[tag]))
                    print("Diff",diff)
                    for i in range(diff):
                        if len(poses) > len(self.duplicates[tag]):
                            self.duplicates[tag].append(self.create_duplicate(tag=tag))


                    if exit_loop:
                        break
                    

                    for j in range(len(poses)):
                        i+=1
                        loc = poses[j][0]
                        if exit_loop:
                            break
                        obj = self.duplicates[tag][j]
                        print("added object",obj.name)
                        print(loc)
                        obj.location = (loc[0],loc[1],loc[2])
                        obj.rotation_euler = (-1.57,0.0,3.14)
                        obj.keyframe_insert(data_path="location",index=-1,frame=frame_nos)
                    
                    self.update_location(unused=self.duplicates[tag][len(poses):],frame_num=frame_nos)
                        

                else:
                    for pose in poses:
                        obj = self.create_duplicate(tag=tag)
                        loc = pose[0]
                        print("added object",obj.name)
                        print(loc)
                        obj.location = (loc[0],loc[1],loc[2])
                        obj.keyframe_insert(data_path="location",index=-1,frame=frame_nos)
                        self.update_location([obj],frame_num=frame_nos+21)
                        # bpy.context.view_layer.objects.active = obj
                        # temp = bpy.context.active_object
                        # temp.hide_set(True)
                        # obj.keyframe_insert(data_path="hide",index=-1,frame=frame_nos+1)
                        # obj.hide_render = True
                        # obj.keyframe_insert(data_path="hide_render", index=-1)
        #                update_location(obj=obj)
        #                bpy.data.objects.remove(obj)
        #                bpy.context.collection.objects.unlink(obj)
                        

                if i > 50:
                    exit_loop = True

def main():
    bln = Blender()
    bln.set_camera()
    bln.run()

if __name__ == "__main__":
    main()