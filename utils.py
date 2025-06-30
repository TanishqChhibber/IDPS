# utils.py
import time
import csv
import os

def ip_to_int(ip):
    try:
        parts = ip.split(".")
        return sum(int(parts[i]) << (8 * (3 - i)) for i in range(4))
    except Exception as e:
        print(f"[ERROR] Failed to convert IP {ip} to int: {e}")
        return 0

def save_accuracy_log(accuracy, filename="results.csv"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Accuracy"])
        writer.writerow([timestamp, f"{accuracy:.2f}"])
