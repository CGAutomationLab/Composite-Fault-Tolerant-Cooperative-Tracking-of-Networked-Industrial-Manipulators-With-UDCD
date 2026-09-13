Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays
Notice 1: This repository provides the ROS 2 / Gazebo experimental implementation corresponding to the manuscript entitled “Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays.”
Notice 2: The current repository is provided for experimental reproducibility and peer review. It contains a runnable binary implementation of the proposed method together with the required ROS 2 launch files, controller configurations, robot descriptions, and simulation runtime files. The complete source code of the proposed observer and controller will be released after the paper is formally published.
Notice 3: The experiments provided in this repository are ROS 2 / Gazebo simulations using four six-DOF UR5e industrial manipulators and should not be interpreted as physical-hardware experiments.
---
1. Overview
This repository reproduces the experimental study of the paper
> **Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays**
The experimental platform mainly consists of:
a Gazebo Harmonic industrial workcell containing four UR5e manipulators;
four ROS 2 `controller_manager` instances and joint-effort interfaces;
a distributed observer under unknown dynamic communication delays;
four cooperative tracking controllers;
ROS 2 communication and data interfaces for experimental execution and result reproduction.
For the current review version, the core C++ implementation of the proposed observer and tracking controller is distributed in compiled form. The complete source code will be released after publication.
---
2. ROS 2 and UR5e Experimental Platform
2.1 ROS 2
The experimental implementation is developed using ROS 2 Jazzy Jalisco.
ROS 2 provides a modern distributed robotic software framework based on DDS communication and is particularly suitable for networked multi-robot and multi-manipulator systems. Compared with the first-generation ROS architecture, ROS 2 provides improved support for distributed communication, configurable Quality-of-Service policies, multiple robot namespaces, modular hardware interfaces through `ros2_control`, and close integration with modern Gazebo releases.
These characteristics make ROS 2 suitable for implementing the distributed observer, cooperative tracking controller, multi-manipulator communication, and joint-effort control architecture considered in this work.
2.2 UR5e Industrial Manipulator
The simulation platform uses four Universal Robots UR5e manipulators.
UR5e is a widely used six-degree-of-freedom collaborative industrial manipulator with mature ROS 2 support. Universal Robots provides official ROS 2 robot descriptions, drivers, and Gazebo simulation packages, which makes the UR5e platform suitable for reproducible industrial-manipulator control experiments.
The experiments in this repository are performed using UR5e models in Gazebo rather than physical UR5e hardware.
---
3. System Requirements
The release is prepared for the following software environment:
Operating System: Ubuntu 24.04 LTS (Noble Numbat)
ROS Distribution: ROS 2 Jazzy Jalisco
Recommended ROS Installation: ROS 2 Jazzy Desktop Full
Simulation Environment: Gazebo Harmonic / Gazebo Sim 8
CPU Architecture: amd64 / x86_64
Robot Model: Universal Robots UR5e
For this project, the ROS 2 Jazzy Desktop Full installation is recommended:
```bash
sudo apt update
sudo apt install ros-jazzy-desktop-full
```
The `desktop_full` variant includes the ROS 2 desktop environment together with simulation-related packages and the ROS--Gazebo integration required for the Jazzy / Gazebo Harmonic ecosystem.
The official ROS 2 Jazzy installation guide for Ubuntu 24.04 is available at:
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
After installation, initialize the ROS 2 environment using:
```bash
source /opt/ros/jazzy/setup.bash
```
---
4. Install Additional Dependencies and UR5e Packages
After ROS 2 Jazzy Desktop Full has been installed, install the additional packages required by this project:
```bash
sudo apt update

sudo apt install \
  git \
  ros-jazzy-ros-gz \
  ros-jazzy-gz-ros2-control \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-controller-manager \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-ur \
  ros-jazzy-ur-description \
  ros-jazzy-ur-simulation-gz
```
The official Universal Robots ROS 2 documentation is available at:
https://docs.universal-robots.com/Universal_Robots_ROS_Documentation/jazzy/
The official Universal Robots ROS 2 driver repository is:
https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver
For the experiments in this repository, no physical UR5e robot, robot IP address, External Control URCap, or real-robot calibration file is required.
---
5. Clone the Repository
Clone this repository directly as `paper_demo_ws` in the home directory:
```bash
cd ~

git clone https://github.com/CGAutomationLab/XXXX.git paper_demo_ws
```
Enter the workspace:
```bash
cd ~/paper_demo_ws
```
> **Note:** Replace `https://github.com/CGAutomationLab/XXXX.git` with the final repository address of this paper.
The current review package provides the precompiled experimental implementation, so rebuilding the protected observer and controller source code is not required.
---
6. Run the Experiment
The experiment is executed using four terminals.
Before running a launch file in each new terminal, initialize the ROS 2 environment and the provided workspace:
```bash
cd ~/paper_demo_ws

source /opt/ros/jazzy/setup.bash

export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```
The recommended startup sequence is:
```text
Terminal 1: Start the digital simulation platform
Terminal 2: Start the distributed observers
Terminal 3: Activate the joint-effort controllers
Terminal 4: Start the cooperative tracking controllers
```
6.1 Terminal 1 — Start the Digital Simulation Platform
Open the first terminal, initialize the environment as described above, and run:
```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_ur5e_industrial.launch.py
```
This launch file starts the Gazebo industrial workcell, the four UR5e manipulators, the ROS 2 / Gazebo interfaces, and the corresponding `ros2_control` infrastructure.
Wait until all four UR5e manipulators have been loaded before continuing.
6.2 Terminal 2 — Start the Distributed Observers
Open a second terminal, initialize the environment, and run:
```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_delay_observers.launch.py
```
This launch file starts the four distributed observer nodes used in the proposed cooperative control framework.
Keep this terminal running.
6.3 Terminal 3 — Activate the Joint-Effort Controllers
Open a third terminal, initialize the environment, and run:
```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_effort_controllers.launch.py
```
This launch file activates the joint-effort controller of each UR5e manipulator.
After the four effort controllers have been activated, continue to the tracking-control stage.
6.4 Terminal 4 — Start the Cooperative Tracking Controllers
Open a fourth terminal, initialize the environment, and run:
```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_tracking_controllers.launch.py
```
The four networked UR5e manipulators will then execute the cooperative tracking experiment.
To terminate the experiment, use `Ctrl+C` in the running terminals.
---
7. Reproducibility and Source-Code Availability
The current review repository is intended to allow reviewers to reproduce the experimental results reported in the manuscript while protecting the complete research implementation before publication.
The review package provides the executable implementation and all runtime files required for the ROS 2 / Gazebo experiments.
The complete source code of the proposed observer, cooperative tracking controller, and associated experimental implementation will be made publicly available in this repository after the paper is formally published.
Until then, the current repository should be regarded as a reproducible binary implementation of the experimental section of the manuscript.
