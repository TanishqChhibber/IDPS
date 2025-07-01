# auto_trainer.py

from detector import AdvancedAnomalyDetector
from sklearn.metrics import classification_report
from collections import Counter
import time

print("[🚀] Auto Retrainer starting. Evaluating every 10s...")

while True:
    try:
        detector = AdvancedAnomalyDetector()
        detector.load_data()
        detector.train()

        y_pred_raw = detector.model.predict(detector.data)
        y_pred = [1 if x == -1 else 0 for x in y_pred_raw]
        y_true = detector.labels

        print("\n[📊] Evaluation:")
        print("Ground Truth :", Counter(y_true))
        print("Predictions  :", Counter(y_pred))
        print(classification_report(y_true, y_pred, digits=4))
        
        time.sleep(10)
    except Exception as e:
        print("[❌] Error:", str(e))
        time.sleep(10)
