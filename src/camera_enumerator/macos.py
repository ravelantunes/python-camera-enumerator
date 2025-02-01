# Copyright (c) 2025 Ravel Antunes
#
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license information.

"""
Module for enumerating cameras on macOS using AVFoundation.

This module defines the `CameraEnumerator` class that leverages PyObjC to
interact with AVFoundation. It provides a method to list available video capture
devices and their supported formats.
"""

from AVFoundation import AVCaptureDevice, AVMediaTypeVideo
from CoreMedia import CMVideoFormatDescriptionGetDimensions
from Foundation import NSObject

from camera_enumerator import Camera


class CameraEnumerator(NSObject):
    """
    Enumerator for cameras using AVFoundation on macOS.

    The `CameraEnumerator` class provides functionality to enumerate video capture
    devices and extract their supported video formats.
    """

    def enumerate_cameras(self) -> list[Camera]:
        """
        Enumerates available video capture devices and retrieves their supported formats.

        For each device, the method extracts the localized name and formats. Each format
        is analyzed to obtain its dimensions and maximum frame rate.

        Returns:
            list[Camera]: A list of Camera objects, each representing a video device with its
            index, name, and a list of available formats.
        """
        devices = AVCaptureDevice.devicesWithMediaType_(AVMediaTypeVideo)
        cameras = []
        for index, device in enumerate(devices):
            camera_name = device.localizedName()
            dimensions = []
            for format in device.formats():
                format_description = CMVideoFormatDescriptionGetDimensions(format.formatDescription())
                if format.videoSupportedFrameRateRanges():
                    fps = int(format.videoSupportedFrameRateRanges()[0].maxFrameRate())
                else:
                    fps = -1
                dimensions.append((format_description.width, format_description.height, fps))
            cameras.append(Camera(index, camera_name, dimensions))
        return cameras