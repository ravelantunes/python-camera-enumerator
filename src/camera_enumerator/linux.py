# Copyright (c) 2025 Ravel Antunes
#
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license information.

"""
Module for enumerating V4L2 camera devices.

This module provides functionality to list available V4L2 camera devices and
their supported video formats using the `v4l2-ctl` command-line utility.
"""

import re
import subprocess
from typing import List, Tuple

from camera_enumerator import Camera


def enumerate_v4l2_devices() -> List[Camera]:
    """
    Enumerates available V4L2 devices and their supported formats.

    This function retrieves a list of camera devices via the `v4l2-ctl --list-devices`
    command, parses the output, and then for each device, retrieves supported formats
    using `v4l2-ctl --list-formats-ext`.

    Returns:
        List[Camera]: A list of Camera objects representing available devices.
    """
    _raise_if_v4l2_not_installed()

    cameras: List[Camera] = []
    try:
        # List all available video devices with detailed info.
        output = subprocess.check_output(['v4l2-ctl', '--list-devices'], text=True)
        cameras = _parse_list_devices(output)
        for camera in cameras:
            ext_output = subprocess.check_output(
                ['v4l2-ctl', '--list-formats-ext', f'/dev/video{camera.index}'],
                text=True
            )
            camera.formats = _parse_device_resolution(ext_output)
    except Exception as e:
        print(f"Error enumerating v4l2 devices: {e}")

    return cameras


def _raise_if_v4l2_not_installed():
    """
    Raises an exception if the v4l2-ctl command is not installed.
    """
    try:
        subprocess.check_output(['v4l2-ctl', '--version'])
    except FileNotFoundError:
        raise Exception("Error: v4l2-ctl not found. Please install the v4l-utils package.")
    except subprocess.CalledProcessError:
        raise Exception("Error: v4l2-ctl failed to run. Please check your installation.")
    return False


def _parse_list_devices(v4l2_output: str) -> List[Camera]:
    """
    Parses the output from `v4l2-ctl --list-devices` to extract camera devices.

    The parsing logic is separated into this function to simplify unit testing without
    monkey-patching subprocess.check_output.

    Parameters:
        v4l2_output (str): The output string from the `v4l2-ctl --list-devices` command.

    Returns:
        List[Camera]: A list of Camera objects parsed from the command output.
    """
    cameras = []
    for device in v4l2_output.strip().split('\n\n'):
        lines = device.strip().split('\n')
        if len(lines) > 2:
            # Use everything before the colon as the camera name.
            name = lines[0].split(':')[0]
            # Extract the index from the device file line (/dev/videoX).
            index_match = re.search(r'/dev/video(\d+)', lines[1])
            if index_match:
                device_index = int(index_match.group(1))
                camera = Camera(device_index, name, [])
                cameras.append(camera)
    return cameras


def _parse_device_resolution(v4l2_ext_output: str) -> List[Tuple[int, int, int]]:
    """
    Parses the output from `v4l2-ctl --list-formats-ext` to extract available resolutions.

    Searches for resolution details and frame rates in the provided output string. Each
    match is converted into a tuple containing (width, height, fps).

    Parameters:
        v4l2_ext_output (str): The output string from the `v4l2-ctl --list-formats-ext` command.

    Returns:
        List[Tuple[int, int, int]]: A list of tuples, each representing a resolution in the
            format (width, height, fps).
    """
    pattern = re.compile(
        r"Size: Discrete (\d+)x(\d+).*?Interval: Discrete [0-9.]+s \(([0-9.]+) fps\)",
        re.DOTALL
    )
    matches = pattern.findall(v4l2_ext_output)
    resolutions = [(int(width), int(height), int(float(fps))) for width, height, fps in matches]
    return resolutions