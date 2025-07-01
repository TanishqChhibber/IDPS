# Intrusion Detection and Prevention System (IDPS)

## Overview
This **Intrusion Detection and Prevention System (IDPS)** is designed to detect and mitigate various network and system-based attacks using machine learning-based anomaly detection, file system monitoring, and real-time system monitoring. The system aims to identify malicious activity, log suspicious behavior, and simulate attacks to test its effectiveness.

## Features
### 1. Attack Simulator
The attack simulation module generates malicious traffic and behaviors to test the effectiveness of the IDPS. It includes:
- **SYN Flood Attack**: Simulates excessive SYN requests to overwhelm a target.
- **UDP Flood Attack**: Sends large amounts of UDP packets to exhaust resources.
- **Slowloris Attack**: Maintains half-open connections to exhaust server resources.
- **ICMP Flood Attack**: Generates excessive ICMP Echo Request packets.
- **SQL Injection Logging**: Detects and logs potential SQL injection attempts.
- **Fake Bot Traffic Generation**: Simulates bot-like activity to detect abnormal behaviors.

- **NOTE**: These attack simulators can be illegal in some cases as it can greatly decrease the wifi speed. So kindly have some sort of permissions before executing it.


### 2. Supervised Anomaly Detection System
A **Machine Learning-based anomaly detection system** using a **Random Forest Classifier** to detect suspicious activities in system logs and network traffic. It includes:
- **Feature extraction** from network traffic and system events.
- **Supervised learning approach** to classify normal and attack traffic using labeled data.
- **Accuracy Calculation**: Evaluates the model's effectiveness by comparing predictions with labeled data and logs accuracy in `accuracy_log.csv`.
- **Live accuracy plotting**: Visualize accuracy in real time using `live_accuracy_plot.py`.

### 3. Filesystem Monitoring System (Future Development)
This module continuously monitors file system changes and logs malicious activities. It detects:
- **File modifications**: Alerts when a file is changed unexpectedly.
- **File creations**: Monitors newly created files.
- **File deletions**: Tracks deleted files for potential malware activities.
- **File movements**: Detects file renaming or relocation attempts.

### 4. Real-time System Monitoring
Monitors processes and network activity to detect abnormal behavior. Includes:
- **Process Monitoring**: Detects unauthorized or suspicious process executions.
- **Network Traffic Analysis**: Inspects network packets for anomalies.
- **System Resource Usage**: Tracks CPU and memory consumption to identify potential attacks.

### 5. Snort Integration (Future Implementation)
- **Connecting IDPS to Snort**: Integrating anomaly detection with Snort for enhanced real-time network intrusion detection.
- **Hybrid Approach**: Combining signature-based and anomaly-based detection for better accuracy.

## Future Improvements
- **Deep Learning Integration**: Implementing autoencoders or LSTMs for advanced anomaly detection.
- **Real-time Threat Intelligence Feeds**: Incorporating external threat intelligence sources to enhance detection capabilities.
- **Automated Attack Mitigation**: Developing countermeasures that respond to detected attacks by blocking IPs or isolating compromised processes.
- **Graph-based Intrusion Detection**: Leveraging graph neural networks (GNNs) for better detection of sophisticated attack patterns.
- **Multi-agent Collaboration**: Enabling communication between multiple IDPS instances for distributed attack detection.
- **Cloud and IoT Security**: Expanding detection capabilities for cloud environments and IoT devices.

## Research Prospects
The IDPS has potential applications in several research areas:
- **Adversarial Attack Resilience**: Studying how adversarial machine learning can be used to evade detection and developing robust defense mechanisms.
- **Explainable AI (XAI) for Intrusion Detection**: Making anomaly detection interpretable and justifiable for security analysts.
- **Federated Learning for Collaborative Threat Detection**: Enabling decentralized learning models for distributed attack detection.
- **Honeypot Integration**: Enhancing detection capabilities by collecting and analyzing attacker tactics using honeypots.
- **Zero-day Attack Detection**: Improving the IDPS's ability to detect previously unseen attacks through dynamic learning models.

## Installation & Usage

### Requirements
- Python (Latest Version)
- scikit-learn
- pandas
- numpy
- faker


### Running the IDPS (Current Workflow)
1. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
2. Install required packages:
   ```powershell
   pip install scikit-learn pandas numpy faker
   ```
3. Generate labeled data by running the attack simulator:
   ```powershell
   python attack_simulator.py
   ```
   This will continuously generate labeled traffic in `idps_data.csv`.
4. Train the supervised model and view accuracy:
   ```powershell
   python training.py
   ```
   This will train a Random Forest model and print a classification report with accuracy.
5. (Optional) Visualize live accuracy:
   ```powershell
   python live_accuracy_plot.py
   ```

## What each of these files do?

- attack_simulator.py: Generates labeled network traffic (normal and various attacks) and writes to `idps_data.csv`.
- conversion.py: Convert your log files into simple csv file for model training (if needed).
- detector.py: (Legacy/optional) Anomaly detection module.
- idps.py: Main IDPS orchestrator.
- monitor.py: Create logs for network analysis and file analysis.
- training.py: Trains a supervised Random Forest model on `idps_data.csv` and prints accuracy/classification report.


**Typical accuracy after training the model with generated and benchmark data is above 85-90%, depending on data quality and balance.**

## Conclusion
This IDPS provides an integrated approach to intrusion detection and prevention, leveraging machine learning, real-time monitoring, and attack simulation. Future enhancements will improve detection accuracy, automation, and resilience against sophisticated cyber threats.

## Note
This is the first stage of IDPS. I have a lot of improvements to do, including connecting my model with Snort for better performance and many more. Also, I will keep the GitHub repository updated!!

## File Descriptions

- **attack_simulator.py**: Simulates various network attacks (SYN Flood, UDP Flood, Slowloris, SQL Injection, Fake Bot Traffic) and logs them. Can run in a continuous loop for ongoing data generation.
- **detector.py**: Main detection engine. Parses logs, labels events, retrains the Isolation Forest anomaly detection model, and logs detection accuracy in real time.
- **idps.py**: Main orchestrator or entry point for the IDPS system.
- **monitor.py**: Additional monitoring utilities or scripts.
- **utils.py**: Utility functions for data processing, feature extraction, and other helper tasks.
- **training.py**: Contains model training logic, may be used by `detector.py` or for manual retraining.
- **dasbard.py**: (Likely a typo for 'dashboard.py') Dashboard code for real-time monitoring of system metrics.
- **terminal_dashboard.py**: Terminal-based dashboard for live monitoring.
- **live_accuracy_plot.py**: Displays a live-updating graph of detection accuracy using matplotlib.
- **conversion.py**: Converts log files into CSV format for model training.

### Data & Log Files
- **attack_logs.txt**: Text log of all simulated attacks.
- **attack_logs.csv**: CSV log of all simulated attacks (structured).
- **idps_data.csv**: Labeled dataset used for model training. Parsed from attack logs.
- **accuracy_log.csv**: Logs detection accuracy over time for monitoring and analysis.
- **network_logs.csv, balanced_logs.csv, fake_bot_traffic.csv, sql_injection_logs.csv**: Additional datasets for training, testing, or simulation.
