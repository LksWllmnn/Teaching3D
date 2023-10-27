@echo on

cd ./CalibrationWebSocket
start cmd /k  "npm install && SET PORT=3001 && npm run dev"

timeout /t 10

cd ../CalibrateInPy
start cmd /k "pip install opencv-python && python arucoPoseEstimation.py"

@REM cd ../
@REM echo Batch-Datei wurde erfolgreich beendet. > success.txt