@echo on

cd ./CalibrationWebSocket
npm install
SET PORT=3001 && npm run dev

cd ./CalibrateInPy
python arucoPoseEstimation.py