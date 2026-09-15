# Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays

**Notice 1:** *This repository provides the ROS 2 / Gazebo experimental implementation corresponding to the manuscript entitled **“Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays.”***

**Notice 2:** *The current repository is provided for experimental reproducibility and peer review. It contains a runnable binary implementation of the proposed method together with the required ROS 2 launch files, controller configurations, UR5e robot descriptions, and simulation runtime files. The complete source code of the proposed observer, cooperative tracking controller, and experimental platform will be released after the paper is formally published.*

**Notice 3:** *The experiments provided in this repository are ROS 2 / Gazebo simulations using four six-DOF UR5e industrial manipulators and should not be interpreted as physical-hardware experiments.*

---

## 1. Overview

This repository reproduces the experimental study of the paper

> **Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays**

The experimental platform mainly consists of:

- a Gazebo Harmonic industrial workcell containing four UR5e manipulators;
- four ROS 2 `controller_manager` instances and joint-effort interfaces;
- four distributed observer nodes under unknown dynamic communication delays;
- four cooperative tracking controller nodes;
- ROS 2 communication and data interfaces for experimental execution and result reproduction.

For the current review version, the core C++ implementation of the proposed observer and cooperative tracking controller is distributed in precompiled binary form. Therefore, rebuilding the protected control implementation from source is not required. The complete source code will be released after publication.

---

## 2. ROS 2 and UR5e Experimental Platform

### 2.1 ROS 2

The experimental implementation is developed using **ROS 2 Jazzy Jalisco**.

ROS 2 provides a modern distributed robotic software framework based on DDS communication and is particularly suitable for networked multi-robot and multi-manipulator systems. It provides distributed communication, configurable Quality-of-Service policies, multiple robot namespaces, modular hardware interfaces through `ros2_control`, and close integration with modern Gazebo releases.

These characteristics make ROS 2 suitable for implementing the distributed observer, cooperative tracking controller, multi-manipulator communication, and joint-effort control architecture considered in this work.

### 2.2 UR5e Industrial Manipulator

The simulation platform uses four **Universal Robots UR5e** manipulators.

UR5e is a widely used six-degree-of-freedom collaborative industrial manipulator with mature ROS 2 support. Universal Robots provides official ROS 2 robot descriptions, drivers, and Gazebo simulation packages, which makes the UR5e platform suitable for reproducible industrial-manipulator control experiments.

The experiments in this repository are performed using UR5e models in Gazebo rather than physical UR5e hardware.

---

## 3. System Requirements

The binary release is prepared and tested for the following environment:

- **Operating System:** Ubuntu 24.04 LTS (Noble Numbat)
- **ROS Distribution:** ROS 2 Jazzy Jalisco
- **Recommended ROS Installation:** ROS 2 Jazzy Desktop Full
- **Simulation Environment:** Gazebo Harmonic / Gazebo Sim 8
- **CPU Architecture:** amd64 / x86_64
- **Robot Model:** Universal Robots UR5e

For this project, the **ROS 2 Jazzy Desktop Full** installation is recommended:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop-full
```

For ROS 2 Jazzy, the `desktop_full` variant provides the desktop, perception, and simulation stacks together with the ROS--Gazebo integration used by the Jazzy / Gazebo Harmonic ecosystem.

The official ROS 2 Jazzy installation guide for Ubuntu 24.04 is available at:

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

After installation, initialize the ROS 2 environment using:

```bash
source /opt/ros/jazzy/setup.bash
```

---

## 4. Install Additional Dependencies and UR5e Packages

After ROS 2 Jazzy Desktop Full has been installed, install the additional runtime packages required by this experimental package:

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

## 5. Clone the Repository

Clone the repository into the home directory as `paper_demo_ws_release`:

```bash
cd ~

git clone https://github.com/CGAutomationLab/XXXX.git paper_demo_ws_release
```

Enter the released workspace:

```bash
cd ~/paper_demo_ws_release
```

> **Note:** Replace `https://github.com/CGAutomationLab/XXXX.git` with the final GitHub address of this paper.

The repository contains the precompiled ROS 2 installation tree under:

```text
paper_demo_ws_release/
└── install/
```

No `colcon build` step is required for the current review release.

---

## 6. Run the Experiment

The complete experiment is executed using four terminals.

Before running a launch file in **each new terminal**, initialize ROS 2 Jazzy and the provided binary workspace:

```bash
cd ~/paper_demo_ws_release

source /opt/ros/jazzy/setup.bash

export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

The experimental startup sequence is:

```text
Terminal 1: Start the digital industrial simulation platform
Terminal 2: Start the four distributed observers
Terminal 3: Activate the four UR5e joint-effort controllers
Terminal 4: Start the four cooperative tracking controllers
```

### 6.1 Terminal 1 — Start the Digital Industrial Simulation Platform

Open the first terminal, initialize the environment as described above, and run:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_ur5e_industrial.launch.py
```

This launch file starts the sealed Gazebo industrial workcell, Gazebo GUI, ROS 2 / Gazebo clock interface, four UR5e manipulators, and the corresponding `ros2_control` infrastructure.

The four UR5e manipulators are initialized sequentially. Wait until all four manipulators have been loaded before starting the following terminals.

### 6.2 Terminal 2 — Start the Distributed Observers

Open a second terminal, initialize the environment, and run:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_delay_observers.launch.py
```

This launch file starts the four distributed observer nodes used by the networked manipulators.

Keep this terminal running during the experiment.

### 6.3 Terminal 3 — Activate the Joint-Effort Controllers

Open a third terminal, initialize the environment, and run:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_effort_controllers.launch.py
```

This launch file activates the joint-effort controller of each UR5e manipulator.

After all four effort controllers have been activated, proceed to the cooperative tracking stage. The activation launch process may terminate after the four controllers are successfully activated; this is normal.

### 6.4 Terminal 4 — Start the Cooperative Tracking Controllers

Open a fourth terminal, initialize the environment, and run:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_tracking_controllers.launch.py
```

This launch file starts the cooperative-start synchronization node and the four tracking controller nodes. The four networked UR5e manipulators will then execute the cooperative tracking experiment for 30s.

To terminate the experiment, use `Ctrl+C` in the running terminals.

---

## 7. Reproducibility and Source-Code Availability

The current review repository is intended to allow reviewers to reproduce the experimental results reported in the manuscript while protecting the complete research implementation before publication.

The review package provides the precompiled executable implementation together with the ROS 2 launch files, controller configuration, UR5e runtime description, and simulation resources required to execute the experiments.

The complete source code of the proposed distributed observer, cooperative tracking controller, and associated experimental implementation will be made publicly available in this repository after the paper is formally published.

Until then, the current repository should be regarded as a reproducible binary implementation of the experimental section of the manuscript.
