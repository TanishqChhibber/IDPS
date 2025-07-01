# generate_data.py

import pandas as pd
import random
import os
import re

OUTPUT_FILE = "idps_data.csv"
ATTACK_LOG = "attack_logs.txt"

def ip():
    return f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_normal(n=1900):
    normal_data = []
    for _ in range(n):
        normal_data.append({
            "src_ip": ip(),
            "dst_ip": ip(),
            "protocol": random.choice(["TCP", "UDP", "ICMP"]),
            "is_anomaly": 0
        })
    print(f"[✅] Generated {n} normal logs.")
    return pd.DataFrame(normal_data)

def parse_attack_logs(n=100):
    if not os.path.exists(ATTACK_LOG):
        print("[⚠️] attack_logs.txt not found.")
        return pd.DataFrame()

    with open(ATTACK_LOG, "r") as f:
        lines = f.readlines()

    attack_data = []
    count = 0
    for line in reversed(lines):
        if count >= n:
            break
        match = re.search(r"(\d+\.\d+\.\d+\.\d+):?(\d+)?", line)
        if match:
            ip_addr = match.group(1)
            attack_data.append({
                "src_ip": ip_addr,
                "dst_ip": "127.0.0.1",
                "protocol": "TCP",
                "is_anomaly": 1
            })
            count += 1

    print(f"[✅] Parsed {len(attack_data)} attack logs.")
    return pd.DataFrame(attack_data)

def save_combined(normal_df, attack_df):
    if attack_df.empty:
        print("[⚠️] No attack data found. Generating fake 5% anomalies...")
        attack_df = pd.DataFrame([
            {"src_ip": ip(), "dst_ip": "127.0.0.1", "protocol": "TCP", "is_anomaly": 1}
            for _ in range(100)
        ])

    combined = pd.concat([normal_df, attack_df], ignore_index=True)
    combined.to_csv(OUTPUT_FILE, index=False, header=False)
    print(f"[✅] Saved {len(combined)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    print("[📥] Generating training dataset...")
    normal_df = generate_normal()
    attack_df = parse_attack_logs()
    save_combined(normal_df, attack_df)
