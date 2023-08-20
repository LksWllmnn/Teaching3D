using UnityEngine;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System;
using Unity.VisualScripting;
using UnityEngine.SceneManagement;

public delegate void CallReceived();

public class DummyCommunicator : MonoBehaviour
{
    event CallReceived _cR;

    [SerializeField]CalibrationData calibrationData;

    private void Start()
    {
        _cR += NextScene;
        //NextScene();
    }

    void NextScene()
    {
        Debug.Log("Next Scene");
        SceneManager.LoadScene("TestMechanics");
    }

    public void StartCalibrating()
    {
        Task.Run(() =>
        {
            StartSocket();
        });

        NextScene();
    }

    private void StartSocket()
    {
        IPAddress ipAddress = IPAddress.Parse("127.0.0.1"); // Use the appropriate IP address
        int port = 12345; // Use an available port

        TcpListener listener = new TcpListener(ipAddress, port);
        listener.Start();

        UnityEngine.Debug.Log("Waiting for a connection...");

        using (TcpClient client = listener.AcceptTcpClient())
        using (NetworkStream stream = client.GetStream())
        {
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string receivedData = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            Debug.Log(receivedData);
            ProcessReceivedData(receivedData);
        }
        _cR();
        listener.Stop();
    }

    private void ProcessReceivedData(string receivedData)
    {
        string[] vectorStrings = receivedData.Split(new string[] { "||" }, StringSplitOptions.None);

        if (vectorStrings.Length == 2)
        {
            Vector3 vector1 = ParseVectorFromString(vectorStrings[0]);
            Vector3 vector2 = ParseVectorFromString(vectorStrings[1]);

            // Now you can use the parsed vectors as needed
            Debug.Log("Parsed Vector 1: " + vector1);
            Debug.Log("Parsed Vector 2: " + vector2);

            

            // Example: Assign the parsed vectors to a Transform's position and rotation
            calibrationData.Position = vector1;
            calibrationData.Rotation = vector2;

            
        }
        else
        {
            Debug.LogError("Received data format is incorrect.");
        }
    }

    private Vector3 ParseVectorFromString(string vectorString)
    {
        vectorString = vectorString.Trim('[', ']');
        string[] components = vectorString.Split(',');
        Debug.Log(components[0]);

        
        
        if (components.Length == 3)
        {
            float x = float.Parse(components[0]) / 100000000;
            float y = float.Parse(components[1]) / 100000000;
            float z = float.Parse(components[2]) / 100000000;
            return new Vector3(x, y, z);
        }
        else
        {
            Debug.LogError("Vector format is incorrect.");
            return Vector3.zero;
        }
    }
}
