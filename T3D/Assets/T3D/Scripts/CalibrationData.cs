using UnityEngine;

[CreateAssetMenu(fileName = "CalibrationData", menuName = "CalibrationData")]
public class CalibrationData : ScriptableObject
{
    public Vector3 Position;
    public Vector3 Rotation;
}
