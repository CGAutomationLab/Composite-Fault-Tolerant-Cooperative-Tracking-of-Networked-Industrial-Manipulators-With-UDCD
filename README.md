# Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays

**Notice 1:** *This repository provides the ROS 2 / Gazebo experimental package corresponding to the manuscript entitled **“Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays.”***

**Notice 2:** *The current repository is intended for reproducibility and peer review. It provides a runnable binary implementation of the proposed observer and tracking controller, together with the required ROS 2 launch files, controller configurations, UR5e robot descriptions, and Gazebo runtime files. The complete controller and observer source code will be released after the paper is formally published.*

**Notice 3:** *The experiments in this repository are ROS 2 / Gazebo simulations using four six-DOF UR5e industrial manipulators. They should not be interpreted as physical-hardware experiments.*

---

## 1. Overview

This repository reproduces the experimental section of the paper

> **Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays**

The experimental platform consists of four networked UR5e industrial manipulators. The implementation includes the following main components:

- a Gazebo Harmonic industrial workcell containing four UR5e manipulators;
- four ROS 2 `controller_manager` instances and joint-effort interfaces;
- a distributed observer with unknown dynamic communication delays;
- four cooperative tracking controllers;
- full-state constraint handling for the manipulator tracking problem;
- composite fault-tolerant compensation for actuator effectiveness loss and additive faults;
- actor--critic-based online approximation used in the proposed controller;
- a common cooperative-start mechanism for synchronizing the four tracking controllers;
- ROS 2 topics and data interfaces used for experimental monitoring and result reproduction.

For the review version, the core C++ control implementation and the Gazebo world source are distributed in compiled form. The Gazebo industrial world is embedded in the runtime executable. The full research source code will be made publicly available after publication.

---

## 2. Why ROS 2 and UR5e Are Used

### 2.1 ROS 2

The implementation is based on **ROS 2 Jazzy Jalisco**.

Compared with the first-generation ROS architecture, ROS 2 provides a more suitable software infrastructure for distributed and multi-robot experiments. In particular, ROS 2 provides DDS-based distributed communication, configurable Quality-of-Service (QoS) policies, native multi-robot namespace support, modern launch and parameter infrastructures, and direct integration with `ros2_control` and current Gazebo releases.

These features are particularly useful in this work because four manipulators, four distributed observers, four tracking controllers, multiple communication links, and multiple `ros2_control` instances must operate simultaneously.

### 2.2 UR5e Industrial Manipulator

The experimental platform uses the **Universal Robots UR5e**, a mainstream six-degree-of-freedom collaborative industrial manipulator.

UR5e is selected because official ROS 2 support, robot descriptions, control interfaces, and simulation packages are available; its six-DOF structure is representative of practical industrial manipulation systems; and it can be naturally integrated with `ros2_control` and Gazebo.

The present repository uses four UR5e manipulators in Gazebo rather than physical UR5e hardware.

---

## 3. System Requirements

The release has been prepared and tested for the following environment:

- **Operating System:** Ubuntu 24.04 LTS (Noble Numbat)
- **ROS Distribution:** ROS 2 Jazzy Jalisco
- **Gazebo:** Gazebo Harmonic / Gazebo Sim 8
- **CPU Architecture:** amd64 / x86_64
- **Robot Model:** Universal Robots UR5e
- **ROS Control Framework:** `ros2_control`
- **Recommended ROS Installation:** ROS 2 Jazzy Desktop
- **Recommended Environment:** Ubuntu desktop session with functional OpenGL graphics support

Before continuing, verify the Ubuntu version:

```bash
lsb_release -a
```

The expected Ubuntu release is:

```text
Ubuntu 24.04 LTS
```

---

## 4. Install ROS 2 Jazzy

The official ROS 2 Jazzy installation guide for Ubuntu is:

https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

ROS 2 Jazzy binary packages are officially provided for Ubuntu 24.04.

### 4.1 Configure the UTF-8 Locale

```bash
locale
sudo apt update
sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale
```

### 4.2 Enable the Ubuntu Universe Repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

### 4.3 Add the ROS 2 Apt Repository

```bash
sudo apt update
sudo apt install curl -y

export ROS_APT_SOURCE_VERSION=$(curl -s \
https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
| grep -F "tag_name" \
| awk -F'"' '{print $4}')

curl -L -o /tmp/ros2-apt-source.deb \
"https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"

sudo dpkg -i /tmp/ros2-apt-source.deb
```

### 4.4 Install ROS 2 Jazzy Desktop

```bash
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
```

Install commonly used ROS development utilities:

```bash
sudo apt install ros-dev-tools
```

Source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Verify the installation:

```bash
ros2 --help
```

---

## 5. Install Gazebo Harmonic and Required Dependencies

This project uses **Gazebo Harmonic**, whose Gazebo Sim major version is 8.

The official Gazebo Harmonic Ubuntu installation guide is:

https://gazebosim.org/docs/harmonic/install_ubuntu/

### 5.1 Install Gazebo Harmonic

```bash
sudo apt update
sudo apt install curl lsb-release gnupg
```

Add the official OSRF Gazebo repository:

```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
```

```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
| sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
```

Install Gazebo Harmonic:

```bash
sudo apt update
sudo apt install gz-harmonic
```

Verify:

```bash
gz sim --versions
```

A Gazebo Sim 8.x installation is expected.

### 5.2 Install ROS 2 / Gazebo / ros2_control Dependencies

```bash
sudo apt update

sudo apt install \
  git \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-jazzy-ros-gz \
  ros-jazzy-gz-ros2-control \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-controller-manager \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher
```

Initialize `rosdep` if it has not previously been initialized:

```bash
sudo rosdep init
rosdep update
```

If `rosdep` reports that it has already been initialized, only `rosdep update` is required.

---

## 6. Install the UR5e ROS 2 Packages

Universal Robots provides official ROS 2 support for the UR family.

The official ROS 2 driver installation documentation is:

https://docs.universal-robots.com/Universal_Robots_ROS_Documentation/jazzy/doc/ur_robot_driver/ur_robot_driver/doc/installation/installation.html

For ROS 2 Jazzy, the official binary installation is recommended.

First source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Install the Universal Robots ROS 2 packages:

```bash
sudo apt update
sudo apt install ros-jazzy-ur
```

Install the UR description and Gazebo simulation packages explicitly:

```bash
sudo apt install \
  ros-jazzy-ur-description \
  ros-jazzy-ur-simulation-gz
```

Verify that the required packages are visible:

```bash
ros2 pkg prefix ur_description
ros2 pkg prefix ur_simulation_gz
ros2 pkg prefix gz_ros2_control
```

Normally these commands should return installation prefixes under:

```text
/opt/ros/jazzy
```

The official Universal Robots ROS 2 driver repository is:

https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver

For the experiments in this repository, no physical UR5e robot, robot IP address, External Control URCap, or real-robot calibration file is required because the experiments are performed entirely in Gazebo.

---

## 7. Clone This Repository

The commands below assume that the repository is cloned directly as:

```text
~/paper_demo_ws
```

Please keep the workspace name **`paper_demo_ws`**.

Clone the repository:

```bash
cd ~
git clone https://github.com/CGAutomationLab/XXXX.git paper_demo_ws
```

Enter the workspace:

```bash
cd ~/paper_demo_ws
```

> **Important:** Replace `https://github.com/CGAutomationLab/XXXX.git` with the final public repository address of this paper.

The review release contains the precompiled implementation required to reproduce the experiments. The core observer and controller C++ source files are intentionally not included in the review package and will be released after publication.

---

## 8. Build / Prepare the Workspace

### 8.1 Current Review Package

For the **current review version**, the observer, controller, cooperative-start node, and sealed Gazebo world server are already compiled.

Therefore, **do not rebuild the protected controller implementation from source**. The reviewer should use the supplied `install/` directory directly.

In every new terminal, initialize the environment with:

```bash
cd ~/paper_demo_ws

source /opt/ros/jazzy/setup.bash

export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Verify that ROS 2 can locate the experimental package:

```bash
ros2 pkg prefix \
fault_tolerant_cooperative_tracking_control
```

The returned path should point to:

```text
~/paper_demo_ws/install
```

Check the available executables:

```bash
ros2 pkg executables \
fault_tolerant_cooperative_tracking_control
```

### 8.2 Source Version After Publication

After publication, the complete C++ source code will be released. At that time, the workspace can be rebuilt using the standard ROS 2 `colcon` workflow.

Install build dependencies if required:

```bash
sudo apt install \
  build-essential \
  cmake \
  python3-colcon-common-extensions \
  libgz-sim8-dev \
  zlib1g-dev
```

Then:

```bash
cd ~/paper_demo_ws
source /opt/ros/jazzy/setup.bash

rosdep update
rosdep install \
  --from-paths src \
  --ignore-src \
  -r \
  -y
```

Build:

```bash
colcon build \
  --merge-install \
  --cmake-args \
  -DCMAKE_BUILD_TYPE=Release
```

After compilation:

```bash
source ~/paper_demo_ws/install/setup.bash
```

The remainder of the launch procedure is the same as the binary review package.

---

## 9. Run the Experimental Platform

The complete experiment is started in four terminals.

The recommended startup order is:

```text
Terminal 1: Gazebo industrial workcell + four UR5e manipulators
Terminal 2: Four effort controllers
Terminal 3: Four distributed observers
Terminal 4: Four cooperative tracking controllers
```

Do not start the tracking controllers before the Gazebo workcell and the four UR5e controller managers have been initialized.

### 9.1 Terminal 1 — Start the Gazebo Industrial Workcell

Open the first terminal and initialize the environment:

```bash
cd ~/paper_demo_ws
source /opt/ros/jazzy/setup.bash
export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Launch the industrial workcell:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_ur5e_industrial.launch.py
```

This launch file starts the sealed Gazebo industrial world server, Gazebo GUI, ROS 2 / Gazebo clock bridge, four UR5e robot-state publishers, four UR5e models, four independent `controller_manager` instances, joint-state broadcasters, and the effort controllers in the initial inactive state.

The four manipulators are initialized sequentially to avoid excessive simultaneous loading of Gazebo and `ros2_control`.

Wait until all four UR5e manipulators have been created before continuing.

An optional controller-status check is:

```bash
for i in 1 2 3 4
do
    echo "========== UR${i} =========="
    ros2 control list_controllers \
        -c /ur${i}/controller_manager
done
```

Before activation, the expected status is approximately:

```text
effort_controller       effort_controllers/JointGroupEffortController  inactive
joint_state_broadcaster joint_state_broadcaster/JointStateBroadcaster  active
```

Keep Terminal 1 running.

### 9.2 Terminal 2 — Activate the Four Effort Controllers

Open a second terminal:

```bash
cd ~/paper_demo_ws
source /opt/ros/jazzy/setup.bash
export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Run:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_effort_controllers.launch.py
```

This launch file activates the joint-effort controller of each UR5e manipulator.

After activation, verify:

```bash
for i in 1 2 3 4
do
    echo "========== UR${i} =========="
    ros2 control list_controllers \
        -c /ur${i}/controller_manager
done
```

The expected state is:

```text
effort_controller       effort_controllers/JointGroupEffortController  active
joint_state_broadcaster joint_state_broadcaster/JointStateBroadcaster  active
```

for UR1--UR4.

If the effort-controller activation launch process terminates normally after all four controllers have been activated, this is expected. The controllers themselves continue to run inside their corresponding `controller_manager` processes.

### 9.3 Terminal 3 — Start the Four Distributed Observers

Open a third terminal:

```bash
cd ~/paper_demo_ws
source /opt/ros/jazzy/setup.bash
export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Launch the distributed observers:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_delay_observers.launch.py
```

An optional check is:

```bash
ros2 node list | grep observer
```

Four observer nodes should be visible.

Observer topics can also be inspected using:

```bash
ros2 topic list | grep observer
```

Keep Terminal 3 running.

### 9.4 Terminal 4 — Start the Four Cooperative Tracking Controllers

Open a fourth terminal:

```bash
cd ~/paper_demo_ws
source /opt/ros/jazzy/setup.bash
export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Launch the four tracking controllers:

```bash
ros2 launch \
fault_tolerant_cooperative_tracking_control \
four_tracking_controllers.launch.py
```

This launch file starts the common cooperative tracking start mechanism and the four UR5e tracking controllers. After the cooperative start condition is satisfied, the four networked manipulators begin the tracking experiment.

---

## 10. Optional Runtime Checks

Check ROS 2 nodes:

```bash
ros2 node list
```

Check observer nodes:

```bash
ros2 node list | grep observer
```

Check all controller states:

```bash
for i in 1 2 3 4
do
    echo "========== UR${i} =========="
    ros2 control list_controllers \
        -c /ur${i}/controller_manager
done
```

Check ROS 2 topics:

```bash
ros2 topic list
```

Check the ROS / Gazebo clock:

```bash
ros2 topic echo /clock --once
```

---

## 11. Stopping the Experiment

The recommended shutdown order is:

1. stop the tracking-controller terminal with `Ctrl+C`;
2. stop the observer terminal with `Ctrl+C`;
3. stop any remaining effort-controller launch process if necessary;
4. finally stop the Gazebo terminal with `Ctrl+C`.

If a Gazebo process remains after an abnormal termination, confirm that no stale simulation process is running before restarting the experiment.

---

## 12. Troubleshooting

### 12.1 `Package ... not found`

Check that ROS 2 Jazzy and the provided workspace have both been sourced:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/paper_demo_ws
export COLCON_CURRENT_PREFIX="$PWD/install"
source "$PWD/install/local_setup.bash"
unset COLCON_CURRENT_PREFIX
```

Then verify:

```bash
ros2 pkg prefix \
fault_tolerant_cooperative_tracking_control
```

### 12.2 `No executable found`

Check:

```bash
ros2 pkg executables \
fault_tolerant_cooperative_tracking_control
```

For the binary review version, the required runtime executables must already exist under:

```text
~/paper_demo_ws/install/lib/fault_tolerant_cooperative_tracking_control/
```

### 12.3 `gz_ros2_control-system: Could not find shared library`

Verify:

```bash
ros2 pkg prefix gz_ros2_control
```

If the package is not found:

```bash
sudo apt update
sudo apt install ros-jazzy-gz-ros2-control
```

### 12.4 Controller Manager Is Not Available

Do not start the effort-controller, observer, or tracking stages before all four UR5e manipulators have completed their Gazebo / `ros2_control` initialization.

Check:

```bash
ros2 control list_controllers \
-c /ur1/controller_manager
```

and repeat for UR2--UR4.

### 12.5 Gazebo GUI Warnings

Depending on the graphics driver and Ubuntu desktop configuration, Gazebo may print Qt/QML or Mesa graphics warnings.

Warnings such as QML binding-loop messages can be non-fatal if the Gazebo GUI opens correctly, the industrial world is visible, all four UR5e manipulators are loaded, `/clock` is being published, and the four controller managers are available.

Errors related to missing Gazebo system plugins, missing ROS packages, missing controller managers, or missing shared libraries should **not** be ignored.

---

## 13. Reproducibility and Source-Code Availability

The current review repository is designed to allow reviewers to reproduce the experimental behavior reported in the manuscript without distributing the protected research implementation before publication.

The review package therefore provides precompiled observer executables, precompiled tracking-controller executables, the cooperative-start executable, the sealed Gazebo industrial world server, ROS 2 launch files, `ros2_control` configuration files, and the required UR5e runtime descriptions.

The review package does not disclose the complete core C++ implementation of the proposed control algorithm or the original Gazebo world source.

After formal publication of the paper, the complete implementation source code will be made publicly available in this repository to support further reproduction, comparison, and academic research.

---

## 14. Citation

If this repository is useful for your research, please cite the corresponding paper after its final bibliographic information becomes available.

```bibtex
@article{XXXX,
  author  = {XXXX},
  title   = {Composite Fault-Tolerant Cooperative Tracking of Networked Industrial Manipulators With Unknown Dynamic Communication Delays},
  journal = {XXXX},
  year    = {XXXX}
}
```

The BibTeX entry will be updated after publication.

---

## 15. Contact

For technical questions related to reproducing the experiments, please open an issue in this repository.

For questions concerning the theoretical derivation or implementation details that are not included in the review package, please refer to the manuscript. The complete source implementation will be released after publication.
