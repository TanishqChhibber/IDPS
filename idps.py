import threading
import subprocess
import time
import os
from training import AdaptiveAnomalyDetector as AnomalyDetector, ip_to_int, LOG_PATH
from monitor import start_system_monitoring
from attack_simulator import scan_and_attack
from detector import load_network_logs, save_model_accuracy

# Globals
DETECTOR = AnomalyDetector()
RUN_ATTACKS = True  # Toggle off if you want no simulation
REALTIME_DASHBOARD = True
BROWSER_DASHBOARD = True


def start_detector_loop():
    print("[IDPS] Detector loop starting...")
    DETECTOR.train_from_logs()
    while True:
        try:
            DETECTOR.train_from_logs()
            DETECTOR.calculate_accuracy()
            save_model_accuracy(DETECTOR.calculate_accuracy())
            time.sleep(10)
        except KeyboardInterrupt:
            print("[IDPS] Stopping detection loop.")
            break


def launch_terminal_dashboard():
    print("[IDPS] Launching terminal dashboard...")
    subprocess.run(["python3", "terminal_dashboard.py"])


def launch_browser_dashboard():
    print("[IDPS] Launching browser dashboard at http://localhost:8050...")
    subprocess.Popen(["python3", "dashboard.py"])


if __name__ == "__main__":
    print("[IDPS] Intrusion Detection & Prevention System Starting...")

    # Optional: Run attack simulation
    if RUN_ATTACKS:
        attack_thread = threading.Thread(target=scan_and_attack, daemon=True)
        attack_thread.start()

    # Monitor processes, network, filesystem
    monitor_thread = threading.Thread(target=start_system_monitoring, daemon=True)
    monitor_thread.start()

    # Run detector
    detector_thread = threading.Thread(target=start_detector_loop, daemon=True)
    detector_thread.start()

    # Launch dashboards
    if REALTIME_DASHBOARD:
        term_dash = threading.Thread(target=launch_terminal_dashboard, daemon=True)
        term_dash.start()

    if BROWSER_DASHBOARD:
        launch_browser_dashboard()
    accuracy = DETECTOR.calculate_accuracy()
if accuracy is not None:
    save_model_accuracy(accuracy)
    print(f"[IDPS] ✅ Current Accuracy: {accuracy * 100:.2f}%")
else:
    print("[IDPS] ⚠️  Accuracy could not be calculated yet.")


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[IDPS] System shutting down.")
