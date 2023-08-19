# Teaching3D
A Repository for a Project to visualise real Classes in 3D with xr and cv technologies


# Develop with this project
1. Get the Azure-Kinect-SDK from Microsoft (it doesn't matte if you get the Binary files from [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md) or the repo from [here](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/tree/develop) you realy just have to get the viewer and recorder) this is not really nessesary but this is helfpful to get some tools to feel into the Azure Kinect.

2. Clone this repo

3. Some of the Library Files from the Azure Kinect SDK for Unity are to big for GitHub. Get those 4 Files from [here](https://bwsyncandshare.kit.edu/s/D5qKpodrQWmnZog)
from the Root Folder set those Files here:


```
Assets/Plugins/onnxruntime_providers_cuda.dll
Assets/Plugins/onnxruntime_providers_cuda.dll.meta
dnn_model_2_0_op11.onnx
onnxruntime_providers_cuda.dll
Packages/Microsoft.Azure.Kinect.BodyTracking.1.1.2/content/dnn_model_2_0_op11.onnx
Packages/Microsoft.Azure.Kinect.BodyTracking.1.1.2/Microsoft.Azure.Kinect.BodyTracking.1.1.2.nupkg
Packages/Microsoft.Azure.Kinect.BodyTracking.ONNXRuntime.1.10.0/lib/native/amd64/release/onnxruntime_providers_cuda.dll
Packages/Microsoft.Azure.Kinect.BodyTracking.ONNXRuntime.1.10.0/Microsoft.Azure.Kinect.BodyTracking.ONNXRuntime.1.10.0.nupkg
```

4. In the Folder CalibrateInPy it is recommendet to set up a venv. OpenCV Version 4.6.0.66 is used. To build an .exe, pyinstaller was used. (Building an exe is nessesary to set this up in unity to calibrate the camera.) If you want to develop inside of the cailbration an you createt a new .exe, set this inside of the path 
```
Assets/Plugins/T3D/exes/
```
Name the exe like the exe there already is or change the path in the Script "Calibrate Manager" and Change the name of the Path.







