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

### 2. Anomaly Detection System
A **Machine Learning-based anomaly detection system** using **Isolation Forest** to detect suspicious activities in system logs and network traffic. It includes:
- **Feature extraction** from network traffic and system events.
- **Unsupervised learning approach** to classify deviations from normal behavior.
- **Threshold-based alerting mechanism** for detected anomalies.
- **Accuracy Calculation**: Evaluates the model's effectiveness by comparing predictions with labeled data.
- **Adaptive Learning**: Continuously updates the model with new data to improve detection accuracy.

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
- Scikit-learn
- Pandas
- NumPy
- TensorFlow/PyTorch (for future deep learning integration)

### Running the IDPS
1. Clone the repository:
   ```bash
   git clone https://github.com/Manavagg2003/Intrusion-Detection-Prevention-System.git
   ```
2. Run the attack simulator:
   ```bash
   python attack_simulator.py
   ```
3. Start the anomaly detection module:
   ```bash
   python detector.py
   ```
4. Finally run your IDS:
   ```bash
   python idps.py
   ```

5. To convert your logs into csv for model training:
   ```bash
   python conversion.py
   ```

6. To train your model:
   ```bash
   python training.py
   ```
**Note**: 
- Now you can just skip part 3 and 4 and just run **python idps.py**
- And also skip part 2 and 6 and just run **python training.py**

## What each of these files do?
- attack_simulator.py: Generates all types of attacks mentioned above.
- conversion.py: Convert your log files into simple csv file for model training.
- detector.py: Start the anomaly detection module.
- idps.py: Main idps.
- monitor.py: Create logs for network analysis and file analysis.
- training.py: To train our isolation forest based idps model. You also get to chose if you want to start the attack_simulator.py then train the model or not.

**My current accuracy after training the model with benchmark database and self-database after full day of training came out to be 99% for now**

## Conclusion
This IDPS provides an integrated approach to intrusion detection and prevention, leveraging machine learning, real-time monitoring, and attack simulation. Future enhancements will improve detection accuracy, automation, and resilience against sophisticated cyber threats.

## Note
This is the first stage of IDPS. I have a lot of improvements to do, including connecting my model with Snort for better performance and many more. Also, I will keep the GitHub repository updated!!
