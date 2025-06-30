# monitor.py
import psutil
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_abnormal_processes(threshold=50.0):
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > threshold:
                logging.warning(f"High CPU usage: {proc.info['name']} (PID: {proc.info['pid']}) using {proc.info['cpu_percent']}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def log_network_connections():
    conns = psutil.net_connections()
    for conn in conns:
        if conn.status == 'ESTABLISHED' and conn.raddr:
            logging.info(f"Active connection: {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}")

def start_system_monitoring(interval=10):
    logging
