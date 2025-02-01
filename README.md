# Python Enumerate Cameras

A simple utility tool to list cameras connected in a consistent way across different platforms (linux or MacOS).

## Installation

### MacOS
When running on MacOS it will leverage AVFoundation, and make calls leveraging pyobjc bindings.
No additional dependencies are required.

## Linux

On linux, it will use v4l2-ctl to list cameras. Make sure you have v4l-utils installed.
ie.:
```bash
sudo apt-get install v4l-utils
```

## Usage

```python
from camera_enumerator import get_cameras, Camera
cameras: list[Camera] = get_cameras()
for cam in cameras:
    print(f"- Camera {cam.index}: {cam.name}")
    for format in cam.formats:
        print("  %dx%d @ %d fps" % format)
```

Output:
```
- Camera 0: FaceTime HD Camera
  1280x720 @ 30 fps
  640x480 @ 30 fps
```