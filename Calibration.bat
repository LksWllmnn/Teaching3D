@echo on

cd ./CalibrationWebSocket
npm install
start /B cmd /C SET PORT=3001 && npm run dev

cd ./CalibrateInPy
python arucoPoseEstimation.py