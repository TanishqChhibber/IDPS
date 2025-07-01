from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class AdvancedAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=300,
            contamination=0.05,
            max_samples='auto',
            random_state=42,
            verbose=0
        )
        self.data = []
        self.labels = []
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()

    def ip_to_int(self, ip):
        parts = list(map(int, ip.split(".")))
        return sum([parts[i] << (24 - 8*i) for i in range(4)])

    def load_data(self, path="idps_data.csv"):
        df = pd.read_csv(path)
        df.columns = ['src_ip', 'dst_ip', 'protocol', 'is_anomaly']
        if df.empty:
            print("[WARNING] Loaded data is empty.")
            return

        df['src_ip'] = df['src_ip'].apply(self.ip_to_int)
        df['dst_ip'] = df['dst_ip'].apply(self.ip_to_int)

        # Encode protocol
        protocol_map = {"TCP": 1, "UDP": 2, "ICMP": 3}
        df['protocol'] = df['protocol'].map(protocol_map).fillna(0).astype(int)

        # Add dummy port (if needed)
        df['port'] = 80

        X = df[['src_ip', 'dst_ip', 'protocol', 'port']].values
        self.data = self.scaler.fit_transform(X)
        self.labels = df['is_anomaly'].astype(int).values

    def train(self):
        if len(self.data) == 0:
            raise ValueError("No data loaded!")
        print("[INFO] Training with contamination=0.05")
        self.model.fit(self.data)

    def predict(self):
        raw_preds = self.model.predict(self.data)
        return [1 if x == -1 else 0 for x in raw_preds]
