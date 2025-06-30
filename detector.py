# detector.py

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time
import csv
import os
import re

DATA_PATH = "idps_data.csv"
LOG_PATH = "results.csv"
ACCURACY_LOG = "accuracy_log.csv"

class AdvancedAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.data = []
        self.labels = []

    def ip_to_int(self, ip):
        try:
            parts = ip.split(".")
            return sum(int(parts[i]) << (8 * (3 - i)) for i in range(4))
        except Exception:
            return 0

    def load_data(self):
        if not os.path.exists(DATA_PATH):
            print("[WARNING] No data found to load.")
            return
        try:
            df = pd.read_csv(DATA_PATH, on_bad_lines='skip')  # Skips bad lines (pandas >=1.3)
        except TypeError:
            # For older pandas versions
            df = pd.read_csv(DATA_PATH, error_bad_lines=False)
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            return
        if df.empty:
            return
        df['src_ip'] = df['src_ip'].apply(self.ip_to_int)
        df['dst_ip'] = df['dst_ip'].apply(self.ip_to_int)
        self.data = df[['src_ip', 'dst_ip', 'protocol']].values
        self.labels = df['is_anomaly'].values

    def train(self):
        if len(self.data) < 10:
            print("[INFO] Not enough data to train.")
            return

        self.model.fit(self.data)
        print("[INFO] Model trained on latest data.")

    def detect(self):
        if len(self.data) == 0:
            print("[WARNING] No data to detect from.")
            return

        predictions = self.model.predict(self.data)
        predictions = np.where(predictions == -1, 1, 0)
        accuracy = np.mean(self.labels == predictions)
        print(f"[INFO] Detection Accuracy: {accuracy * 100:.2f}%")
        return accuracy

    def log_accuracy(self, accuracy):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        file_exists = os.path.exists(ACCURACY_LOG)
        with open(ACCURACY_LOG, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Accuracy"])
            writer.writerow([timestamp, f"{accuracy * 100:.2f}"])

    def train_from_logs(self):
        self.load_data()
        self.train()
        acc = self.detect()
        if acc is not None:
            self.log_accuracy(acc)

def load_network_logs(path=DATA_PATH):
    if not os.path.exists(path):
        print(f"[ERROR] File {path} not found.")
        return pd.DataFrame()

    df = pd.read_csv(path)
    if df.empty:
        print(f"[WARNING] File {path} is empty.")
    return df

def save_model_accuracy(accuracy, path=ACCURACY_LOG):
    if accuracy is None:
        print("[WARNING] Tried to save None accuracy.")
        return
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(path)

    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Accuracy"])
        writer.writerow([timestamp, f"{accuracy * 100:.2f}"])

def parse_attack_logs(log_path="attack_logs.txt", data_path=DATA_PATH):
    if not os.path.exists(log_path):
        return
    # Read all logs
    with open(log_path, "r") as f:
        lines = f.readlines()
    data = []
    for line in lines:
        m = re.search(r"(\d+\.\d+\.\d+\.\d+):?(\d+)?", line)
        if m:
            ip = m.group(1)
            port = int(m.group(2)) if m.group(2) else 0
            if "Attack" in line:
                label = 1  # anomaly
            else:
                label = 0  # normal
            # You can expand features as needed
            data.append({
                "src_ip": ip,
                "dst_ip": "127.0.0.1",
                "protocol": "TCP",
                "port": port,
                "is_anomaly": label
            })
    if data:
        df = pd.DataFrame(data)
        if os.path.exists(data_path):
            df.to_csv(data_path, mode='a', header=False, index=False)
        else:
            df.to_csv(data_path, index=False)

# Run detector directly
if __name__ == "__main__":
    detector = AdvancedAnomalyDetector()
    while True:
        parse_attack_logs()
        detector.load_data()
        detector.train()
        acc = detector.detect()
        if acc is not None:
            detector.log_accuracy(acc)
            print(f"[INFO] Logged accuracy: {acc * 100:.2f}%")
        else:
            print("[INFO] Accuracy could not be calculated this cycle.")
        print("[INFO] Detector cycle complete. Waiting 10 seconds before next round...")
        time.sleep(10)
