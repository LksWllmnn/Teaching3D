using System.Collections.Generic;
using UnityEngine;
using Microsoft.Azure.Kinect.Sensor;
using TMPro;
using System;

public class CaliView : MonoBehaviour
{
    List<Device> _devices;
    [SerializeField] TMP_Dropdown _drop;
    [SerializeField] GameObject _pcSelectButton;
    [SerializeField] GameObject _noDevicesText;
    [SerializeField] GameObject _pcSelectionSpace;


    public void StartView(List<Device> devices)
    {
        _devices = devices;
        ShowInDropDown();
        CreatSelectButtons();
    }

    public void ChangedDropSelect(Int32 i)
    {
        Debug.Log("Used Selection: " + i);
    }

    void ShowInDropDown()
    {
        List<string> options = new List<string>();
        if(_devices.Count > 0)
        {
            options.Add("(Select)");
            foreach (Device device in _devices)
            {
                options.Add(device.SerialNum);
            }
        } else
        {
            options.Add("no Devices");
        }
        Debug.Log(_drop);
        _drop.AddOptions(options);
    }
    
    void CreatSelectButtons()
    {
        if(_devices.Count == 0)
        {
            GameObject go = Instantiate(_noDevicesText, _pcSelectionSpace.transform);
        } else if( _devices.Count > 1)
        {
            for(int i = 0; i < _devices.Count; i++)
            {
                GameObject selectButton = Instantiate(_pcSelectButton, _pcSelectionSpace.transform);
                selectButton.GetComponent<RectTransform>().anchorMax = new Vector2(0.5f, 1);
                selectButton.GetComponent<RectTransform>().anchorMin = new Vector2(0.5f, 1);
                selectButton.GetComponent<RectTransform>().anchoredPosition = new Vector2(0, -30 - i * 35);
                selectButton.transform.GetChild(0).GetComponent<TMP_Text>().text = "Show PC " + i;
            }

            GameObject selectAllButton = Instantiate(_pcSelectButton, _pcSelectionSpace.transform);
            selectAllButton.GetComponent<RectTransform>().anchorMax = new Vector2(0.5f, 0);
            selectAllButton.GetComponent<RectTransform>().anchorMin = new Vector2(0.5f, 0);
            selectAllButton.GetComponent<RectTransform>().anchoredPosition += new Vector2(0, 20f);
            selectAllButton.transform.GetChild(0).GetComponent<TMP_Text>().text = "Show All PCs";

        } else if (_devices.Count == 1) {
            GameObject selectButton = Instantiate(_pcSelectButton, _pcSelectionSpace.transform);
            selectButton.GetComponent<RectTransform>().anchorMax = new Vector2(0.5f, 1);
            selectButton.GetComponent<RectTransform>().anchorMin = new Vector2(0.5f, 1);
        }
    }

}
