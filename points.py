import numpy as np
import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import csv
import torch
from PIL import Image



class Camera_xyz():
    def __init__(self) -> None:
        self.props = None
        file_path = ".\calibration.npz"
        self.props = np.load(file=file_path)

        self.R_mtx = np.identity(3)
        self.t_vec = np.array([0,2,0])
        self.Rt = np.column_stack((self.R_mtx,self.t_vec))
        self.scaling_factor = None

        self.inv_cam_mtx = np.linalg.inv(self.props['new_mtx'])
        self.inv_R_mtx = np.linalg.inv(self.R_mtx)

    def calculate_XYZ(self,u,v,s):
                                      
        #Solve: From Image Pixels, find World Points
        self.scaling_factor = s
        uv_1=np.array([[u,v,1]], dtype=np.float32)
        uv_1=uv_1.T
        suv_1 = self.scaling_factor*uv_1
        xyz_c = self.inv_cam_mtx.dot(suv_1)
        xyz_c = xyz_c-self.t_vec
        XYZ = self.inv_R_mtx.dot(xyz_c)

        return XYZ
    

class Extract():
    def __init__(self) -> None:
        version="v1"
        backbone="ViTL14"
        self.model_unidepth = torch.hub.load("lpiccinelli-eth/UniDepth", "UniDepth", version=version, backbone=backbone, pretrained=True, trust_repo=True, force_reload=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_unidepth = self.model_unidepth.to(self.device)
        self.final_loc = Camera_xyz()

        self.model_yolo=YOLO('yolov9c.pt')
        self.csv_file_path = "output.csv"

        self.class_list = ['BashMesh_Man_Simp', 'roadbike 2.0.1', 'Car', 'B_Wheel', 'airplane', 'bus',
                      'train', 'truck', 'boat', 'Traffic_signal1', 'absperrhut', 'stop sign', 'parking meter',
                      'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
                      'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
                      'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                      'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
                      'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
                      'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
                      'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

        # self.tracker=CustomTracker()

        self.cap = cv2.VideoCapture(r".\\P3Data\\P3Data\Sequences\scene9\\Undist\\2023-03-04_17-20-36-front_undistort.mp4")

        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    def get_depth(self,frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Load the RGB image and the normalization will be taken care of by the model
        rgb = torch.from_numpy(np.array(frame_rgb)).permute(2, 0, 1) # C, H, W

        predictions = self.model_unidepth.infer(rgb)

        # Metric Depth Estimation
        depth = predictions["depth"]

        return depth[0][0]

    def get_bounding_box(self):
        i = 0
        frames = []
        inferences = []
        num_identified = []
        while i<800:
            i+=1
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.model_yolo.predict(frame)

            frames.append(frame)
            inferences.append(results)
            temp = results[0].boxes.shape
            num_identified.append(temp[0])

            if i%10 == 0:

                items = max(num_identified)
                pos = num_identified.index(items)

                results = inferences[pos]

                scale = self.get_depth(frame=frames[pos])


                a = results[0].boxes.data
                a = a.detach().cpu().numpy()
                px = pd.DataFrame(a).astype("float")
                # print(px)

                with open(self.csv_file_path, mode="a") as file:
                    writer = csv.writer(file)

                    for index, row in px.iterrows():
                        #        print(row)
                        x1 = int(row[0])
                        y1 = int(row[1])
                        x2 = int(row[2])
                        y2 = int(row[3])
                        d = int(row[5])
                        c = self.class_list[d]
                        # clist.append(c)
                        # if 'car' in c:
                        # list.append([x1, y1, x2, y2])
                        cx = int(x1 + x2) // 2
                        cy = int(y1 + y2) // 2
                        sfactor = scale[cx][cy]
                        xyz = self.final_loc.calculate_XYZ(u=cx,v=cy,s=sfactor)
                        writer.writerow([xyz,c])


                # bbox_id = self.tracker.custom_update(list)
                
                    # writer.writeheader()
                # print(bbox_id)
                    # for bbox,cls in zip(bbox_id,clist):
                        # x3, y3, x4, y4, id = bbox
                        
                        # cv2.circle(frame,(cx,cy),4,(0,0,255),-1) #draw ceter points of bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                        # cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)

                frames = []
                inferences = []
                num_identified = []
            else:
                continue

def main():
    obj = Extract()
    obj.get_bounding_box()

if __name__ == "__main__":
    main()