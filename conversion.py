import re
import pandas as pd

log_file = "./logs/network_connections_log.txt"

pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - addr\(ip='([\d\.]+)', port=(\d+)\) -> addr\(ip='([\d\.]+)', port=(\d+)\) - (\w+)")

data = []
with open(log_file, "r") as file:
    for line in file:
        match = pattern.search(line)
        if match:
            timestamp, src_ip, src_port, dest_ip, dest_port, state = match.groups()
            data.append([timestamp, src_ip, int(src_port), dest_ip, int(dest_port), state])

df = pd.DataFrame(data, columns=["Timestamp", "Source_IP", "Source_Port", "Dest_IP", "Dest_Port", "State"])

df.to_csv("network_logs.csv", index=False)
print("Data saved successfully!")
