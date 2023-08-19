using Microsoft.Azure.Kinect.Sensor;
using System.Collections.Generic;
using UnityEngine;

public class PointCloudManager : MonoBehaviour
{
    List<Device> _devices;
    [SerializeField] GameObject _pc;
    [SerializeField] GameObject _pcEmpty;
    [SerializeField] CaliView _caliView;
    // Start is called before the first frame update
    void Start()
    {
        _devices = new List<Device>();
        for (int i = 0; i < Device.GetInstalledCount(); i++)
        {
            _devices.Add(Device.Open(i));
            GameObject pc = Instantiate(_pc, _pcEmpty.transform);
            pc.GetComponent<pointcloud>().DeviceNumber = i;
            pc.GetComponent<pointcloud>().StartPC(_devices[i], CreateRandomRGBColor());
        }
        _caliView.StartView(_devices);
    }

    Color CreateRandomRGBColor()
    {
        return new Color(Random.value, Random.value, Random.value);
    }

}
