# Copyright (c) 2025 Ravel Antunes
#
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license information.

"""
Mocks the call to subprocess.check_output to a hardcoded response, so tests can be run without a camera
"""
from camera_enumerator import _parse_device_resolution, _parse_list_devices


def test_enumerate_v4l2_devices():
    # Mock the call to subprocess.check_output
    sample_output = '''ZED: ZED (usb-0000:00:14.0-1):
        /dev/video2
        /dev/video3

BisonCam,NB Pro: BisonCam,NB Pr (usb-0000:00:14.0-8):
        /dev/video0
        /dev/video1'''

    # Call the function to test
    devices = _parse_list_devices(sample_output)

    # Check the result
    assert len(devices) == 2
    assert devices[0].index == 2
    assert devices[0].name == 'ZED'
    assert devices[1].index == 0
    assert devices[1].name == 'BisonCam,NB Pro'


def test_enumerate_v4l2_devices_empty():
    assert len(_parse_list_devices('')) == 0


def test_resolutions_parsing():
    sample_output = '''
    ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'MJPG' (Motion-JPEG, compressed)
            Size: Discrete 1280x720
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 640x480
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 640x360
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 352x288
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 320x240
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 176x144
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 160x120
                Interval: Discrete 0.033s (30.000 fps)
        [1]: 'YUYV' (YUYV 4:2:2)
            Size: Discrete 1280x720
                Interval: Discrete 0.100s (10.000 fps)
            Size: Discrete 640x480
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 640x360
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 352x288
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 320x240
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 176x144
                Interval: Discrete 0.033s (30.000 fps)
            Size: Discrete 160x120
                Interval: Discrete 0.033s (30.000 fps)
    '''
    resolutions = _parse_device_resolution(sample_output)
    assert len(resolutions) == 14
    assert resolutions[0] == (1280, 720, 30)
    assert resolutions[1] == (640, 480, 30)
    assert resolutions[2] == (640, 360, 30)
    assert resolutions[3] == (352, 288, 30)
    assert resolutions[4] == (320, 240, 30)
    assert resolutions[5] == (176, 144, 30)
