using UnityEngine;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Net.Sockets;
using System.Net;
using System.Text;
using Unity.VisualScripting;

public class CalibrateManager : MonoBehaviour
{
    [InspectorLabel("Name of the exe to calibrate cameras (without .exe)")]
    [SerializeField] string _nameExe;

    public void StartCalibrating()
    {
        Task.Run(() =>
        {
            StartSocket();
        });
        StartExe();
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
            UnityEngine.Debug.Log("Received data: " + receivedData);
        }

        listener.Stop();
    }

    private void StartExe()
    {
        Process.Start(Application.dataPath + $"/T3D/exes/{_nameExe}.exe");
    }
}
