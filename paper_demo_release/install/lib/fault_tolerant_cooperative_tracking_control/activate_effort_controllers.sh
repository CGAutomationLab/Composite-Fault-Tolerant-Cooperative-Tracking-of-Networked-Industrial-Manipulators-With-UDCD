#!/usr/bin/env bash
set -euo pipefail

for robot_id in 1 2 3 4
do
  controller_manager="/ur${robot_id}/controller_manager"

  echo "Waiting for ${controller_manager} ..."

  until ros2 control list_controllers \
    -c "${controller_manager}" >/dev/null 2>&1
  do
    sleep 0.1
  done

  echo "Activating /ur${robot_id}/effort_controller ..."

  while true
  do
    controller_list="$(
      ros2 control list_controllers \
        -c "${controller_manager}" 2>/dev/null || true
    )"

    if printf '%s\n' "${controller_list}" | \
      grep -Eq '^effort_controller[[:space:]].*[[:space:]]active[[:space:]]*$'
    then
      break
    fi

    ros2 control set_controller_state \
      effort_controller \
      active \
      -c "${controller_manager}" >/dev/null 2>&1 || true

    sleep 0.1
  done

  echo "/ur${robot_id}/effort_controller is active."
done

echo "All four effort controllers are active."
