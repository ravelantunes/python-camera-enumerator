# Copyright (c) 2025 Ravel Antunes
#
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license information.

"""
Module for representing a camera device.

This module defines the `Camera` class which encapsulates basic information
about a camera including its index, name, and available video formats.
Each available format is a tuple of (width, height, fps).
"""

import platform
from typing import List, Tuple

class Camera:
    """
    Represents a camera with an index, name, and supported video formats.

    Attributes:
        index (int): Unique identifier for the camera. It's also the index for the camera device on opencv.
        name (str): Descriptive name for the camera.
        formats (List[Tuple[int, int, int]]): List of available formats as
            tuples, where each tuple contains (width, height, fps).
    """
    index: int
    name: str
    formats: List[Tuple[int, int, int]]

    def __init__(self, index: int, name: str, formats: List[Tuple[int, int, int]]):
        """
        Initializes a new Camera instance.

        Args:
            index (int): The camera's unique index.
            name (str): The camera's name.
            formats (List[Tuple[int, int, int]]): List of available video formats.
        """
        self.index = index
        self.name = name
        self.formats = formats

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the camera.

        Returns:
            str: The name of the camera.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the camera,
        including available formats.

        Returns:
            str: A string representation of the camera and its formats.
        """
        formats_str = "\n".join(
            [f"\t{w}x{h}@{fps}fps" for w, h, fps in self.formats]
        )
        return f"Camera({self.index}, {self.name})\nAvailable Formats:\n{formats_str}"


def _is_mac_os():
    return platform.system() == 'Darwin'


def _is_windows_os():
    return platform.system() == 'Windows'


def _is_linux_os():
    return platform.system() == 'Linux'


def get_cameras():
    if _is_mac_os():
        return _mac_os()
    elif _is_windows_os():
        print('Windows OS')
    elif _is_linux_os():
        print('Linux OS')
    else:
        print('Unknown OS')


def _mac_os() -> list[Camera]:
    from camera_enumerator.macos import CameraEnumerator
    enumerator = CameraEnumerator.alloc().init()
    cameras = enumerator.enumerate_cameras()
    return cameras

