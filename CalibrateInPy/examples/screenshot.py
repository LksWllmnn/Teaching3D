import cv2

cap = cv2.VideoCapture(0)

num = 0

def snap():
    global num
    screenshot_filename = f"screenshot{num}.jpg"
    num = num + 1
    cv2.imwrite(screenshot_filename, frame)
    print(f"Screenshot saved as {screenshot_filename}")

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        snap()
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()