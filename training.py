import os
import time
import csv
import json
import threading
import psutil
import nmap
import scapy.all as scapy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sklearn.ensemble import IsolationForest
import numpy as np
from collections import deque

DATASET_PATH = "network_logs.csv"
LOG_PATH = "idps_data.csv"

def ip_to_int(ip):
    """Convert IP address to integer for machine learning processing"""
    parts = ip.split(".")
    return sum(int(parts[i]) << (8 * (3 - i)) for i in range(4))

def load_existing_data(file=LOG_PATH):
    """Loads past dataset for improved training & accuracy evaluation"""
    data, labels = [], []
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                if len(row) >= 4:
                    data.append([ip_to_int(row[0]), ip_to_int(row[1]), int(row[2])])
                    labels.append(int(row[3]))
    except FileNotFoundError:
        print("[WARNING] No previous dataset found.")
    return data, labels

class NetworkMonitor:
    def __init__(self):
        self.packet_log = []

    def packet_callback(self, packet):
        if packet.haslayer(scapy.IP):
            src_ip = packet[scapy.IP].src
            dst_ip = packet[scapy.IP].dst
            protocol = packet[scapy.IP].proto
            self.packet_log.append([src_ip, dst_ip, protocol])

    def start_monitoring(self):
        print("[INFO] Network monitoring started...")
        scapy.sniff(prn=self.packet_callback, store=False)

class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.event_log = []

    def on_modified(self, event):
        if not event.is_directory:
            self.event_log.append([time.time(), event.src_path, "modified"])

    def start_monitoring(self, path="./"):
        print("[INFO] File monitoring started...")
        observer = Observer()
        observer.schedule(self, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.data = deque(maxlen=500)
        self.labels = deque(maxlen=500)

    def train(self):
        """Train the Isolation Forest model on network data"""
        if len(self.data) > 10:
            X = np.array(self.data)
            self.model.fit(X)
            print("[INFO] Model trained successfully.")

    def detect(self, new_event):
        """Predict if an event is an anomaly (-1) or normal (1)"""
        X_test = np.array([new_event])
        result = self.model.predict(X_test)
        return result[0] == -1

    def add_data(self, event, label):
        self.data.append(event)
        self.labels.append(label)
        self.train()

    def calculate_accuracy(self):
        """Evaluate model accuracy using labeled data"""
        if len(self.data) > 10:
            X = np.array(self.data)
            y_true = np.array(self.labels)  
            y_pred = self.model.predict(X)  
            y_pred = np.where(y_pred == -1, 1, 0)  
            accuracy = np.mean(y_true == y_pred)
            print(f"[INFO] Model Accuracy: {accuracy * 100:.2f}%")
            return accuracy

class AttackSimulator:
    def run_nmap_scan(self, target="127.0.0.1"):
        nm = nmap.PortScanner()
        nm.scan(target, arguments="-p 1-65535 -T4 -A -v")
        return nm.csv()

    def run_scapy_attack(self, target="127.0.0.1"):
        print("[INFO] Sending SYN flood attack...")
        for _ in range(1000):
            scapy.send(scapy.IP(dst=target)/scapy.TCP(dport=80, flags="S"), verbose=False)

def save_to_csv(data, filename=LOG_PATH):
    """Save network logs to a CSV file for training"""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["src_ip", "dst_ip", "protocol", "is_anomaly"])
        for row in data:
            writer.writerow(row + [0]) 

if __name__ == "__main__":
    print("[INFO] Starting Intrusion Detection & Prevention System...")

    attack_choice = input("Do you want to start Attack Simulator? (start/don't): ").strip().lower()

    network_monitor = NetworkMonitor()
    file_monitor = FileMonitor()
    anomaly_detector = AnomalyDetector()

   
    existing_data, existing_labels = load_existing_data()
    anomaly_detector.data.extend(existing_data)
    anomaly_detector.labels.extend(existing_labels)
    anomaly_detector.train()

  
    net_thread = threading.Thread(target=network_monitor.start_monitoring, daemon=True)
    file_thread = threading.Thread(target=file_monitor.start_monitoring, daemon=True)

    net_thread.start()
    file_thread.start()

    if attack_choice == "start":
        attack_sim = AttackSimulator()
        attack_thread = threading.Thread(target=attack_sim.run_scapy_attack, daemon=True)
        attack_thread.start()

    try:
        while True:
            time.sleep(10)
            save_to_csv(network_monitor.packet_log)
            print("[INFO] Data saved to CSV and model is training...")
            anomaly_detector.train()
            anomaly_detector.calculate_accuracy()  
    except KeyboardInterrupt:
        print("[INFO] Stopping IDPS...")
