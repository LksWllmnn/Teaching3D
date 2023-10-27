@echo on

cd ./CalibrationWebSocket
start cmd /k  "SET PORT=3001 && npm run dev"

cd ../CalibrateInPy
start cmd /k "python arucoPoseEstimation.py"


cd ../
echo Batch-Datei wurde erfolgreich beendet. > success.txt