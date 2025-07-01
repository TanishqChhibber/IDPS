# [1] attack_simulator.py (live + mixed traffic)

import random
import time
import csv
from faker import Faker

fake = Faker()
TARGET_IP = "192.168.1.10"

LOG_FILE = "idps_data.csv"


def random_ip():
    return fake.ipv4()

def write_log(src, dst, protocol, label):
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([src, dst, protocol, label])

def simulate_attack():
    attack_type = random.choice(["SYN", "UDP", "SQLi", "Slowloris", "Bot"])
    src_ip = random_ip()
    dst_ip = TARGET_IP

    if attack_type == "SYN":
        protocol = "TCP"
    elif attack_type == "UDP":
        protocol = "UDP"
    elif attack_type == "SQLi":
        protocol = "TCP"
    elif attack_type == "Slowloris":
        protocol = "TCP"
    elif attack_type == "Bot":
        protocol = random.choice(["TCP", "UDP", "ICMP"])
    else:
        protocol = "TCP"

    write_log(src_ip, dst_ip, protocol, 1)
    print(f"[🚨] {attack_type} attack from {src_ip} to {dst_ip}")


def simulate_normal():
    src_ip = random_ip()
    dst_ip = random_ip()
    protocol = random.choice(["TCP", "UDP", "ICMP"])
    write_log(src_ip, dst_ip, protocol, 0)
    print(f"[✅] Normal traffic from {src_ip} to {dst_ip}")


def run_simulation(duration_sec=60, attack_ratio=0.05):
    interval = 1  # 1 second interval
    total_events = duration_sec

    for i in range(total_events):
        if random.random() < attack_ratio:
            simulate_attack()
        else:
            simulate_normal()
        time.sleep(interval)


if __name__ == "__main__":
    print("[🔥] Starting Live Traffic Generator... (press Ctrl+C to stop)")
    try:
        run_simulation(duration_sec=999999, attack_ratio=0.05)
    except KeyboardInterrupt:
        print("[🛑] Simulation stopped by user.")
