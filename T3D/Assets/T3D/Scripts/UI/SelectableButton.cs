using UnityEngine;
using UnityEngine.UI;

public class SelectableButton : MonoBehaviour
{
    bool isSelected = false;

    public void IsClicked()
    {
        isSelected = !isSelected;
        if(isSelected)this.GetComponent<Image>().color = Color.red;
        else this.GetComponent<Image>().color = Color.white;
    }
}
