# Copyright (c) 2025 Ravel Antunes
#
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license information.
from camera_enumerator import Camera
from camera_enumerator.camera import get_cameras
from camera_enumerator import _parse_list_devices

if __name__ == '__main__':
    cameras: list[Camera] = get_cameras()
    for cam in cameras:
        print(f"- Camera {cam.index}: {cam.name}")
        for format in cam.formats:
            print("  %dx%d @ %d fps" % format)
