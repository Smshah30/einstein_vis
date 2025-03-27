# Tesla FSD simulation

This is an attempt to simulate the Tesla FSD display. The video from front camera of Tesla is undistorted and used to detect Lanes, different Vehicles, Road Signs, Human Pose, Motion of Vehicles, Traffic Signs and more using SOTA models. The detections are then simulated in Blender. The pipeline is as follows:

<p align="center">
 <img src="images/Pipeline.png" width = "350"/>
</p>

## Results

Lane and Road Signs detection:
<p align="center">
 <img src="images/Lane_detection.png" width = "350"/>
</p>

Traffic Signal detection:
<p align="center">
 <img src="images/Traffic_Signal.png" width = "350"/>
</p>

Detection of other objects:
<p align="center">
 <img src="images/Cycle.png" width = "350"/>
</p>

Human Pose detection:
<p align="center">
 <img src="images/Human_Pose.png" width = "350"/>
</p>

Optical Flow:
<p align="center">
 <img src="images/Optic_Flow.png" width = "350"/>
</p>

Simulation:
<p align="center">
 <img src="images/Result.gif" width = "350"/>
</p>






