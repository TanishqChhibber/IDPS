# training.py

import numpy as np
from sklearn.ensemble import IsolationForest
from collections import deque
import csv
import time
import os

LOG_PATH = "idps_data.csv"

def ip_to_int(ip):
    parts = ip.split(".")
    return sum(int(parts[i]) << (8 * (3 - i)) for i in range(4))

class AdaptiveAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.data = deque(maxlen=500)
        self.labels = deque(maxlen=500)

    def train(self):
        if len(self.data) > 10:
            self.model.fit(np.array(self.data))
            print("[INFO] Model trained successfully.")

    def detect(self, new_event):
        X = np.array([new_event])
        result = self.model.predict(X)
        if result[0] == -1:
            print(f"[ALERT] Anomaly Detected: {new_event}")
        return result[0]

    def add_data(self, event, label):
        self.data.append(event)
        self.labels.append(label)
        self.train()

    def calculate_accuracy(self):
        if len(self.data) > 10:
            y_pred = self.model.predict(np.array(self.data))
            y_pred = np.where(y_pred == -1, 1, 0)
            y_true = np.array(self.labels)
            accuracy = np.mean(y_true == y_pred)
            print(f"[INFO] Model Accuracy: {accuracy * 100:.2f}%")
            return accuracy

    def train_from_logs(self):
        if hasattr(self, 'load_data'):
            self.load_data()
        if hasattr(self, 'train'):
            self.train()
        if hasattr(self, 'calculate_accuracy'):
            acc = self.calculate_accuracy()
        elif hasattr(self, 'detect'):
            acc = self.detect()
        else:
            acc = None
        if acc is not None and hasattr(self, 'log_accuracy'):
            self.log_accuracy(acc)
