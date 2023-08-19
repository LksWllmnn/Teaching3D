using Microsoft.Azure.Kinect.Sensor;
using UnityEngine;

public class GetMaimCamImage : MonoBehaviour
{
    Device kinect;
    public void StartMainCamImage(Device device)
    {
        kinect = device;
        //Setting the Kinect operation mode and starting it
        kinect.StartCameras(new DeviceConfiguration
        {
            ColorFormat = ImageFormat.ColorBGRA32,
            ColorResolution = ColorResolution.R720p,
            DepthMode = DepthMode.NFOV_Unbinned,
            SynchronizedImagesOnly = true,
            CameraFPS = FPS.FPS30
        });
        
    }
}
