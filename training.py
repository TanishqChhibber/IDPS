# training.py (supervised setup)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from collections import Counter
import pandas as pd
import numpy as np

def ip_to_int(ip):
    try:
        parts = list(map(int, ip.split(".")))
        return sum([parts[i] << (8 * (3 - i)) for i in range(4)])
    except:
        return 0

def main():
    print("[🚀] Training supervised model on labeled attack data...")

    df = pd.read_csv("idps_data.csv")
    df.columns = ['src_ip', 'dst_ip', 'protocol', 'is_anomaly']  # add this if no headers

    df['src_ip'] = df['src_ip'].apply(ip_to_int)
    df['dst_ip'] = df['dst_ip'].apply(ip_to_int)

    proto_map = {"TCP": 1, "UDP": 2, "ICMP": 3}
    df['protocol'] = df['protocol'].map(proto_map).fillna(0).astype(int)

    df['port'] = 80
    df['payload_size'] = np.random.randint(40, 1600, size=len(df))
    df['duration'] = np.random.rand(len(df)) * 10



    # Inject controlled adversarial patterns into a subset of attack samples
    np.random.seed(42)
    attack_idx = df['is_anomaly'] == 1
    adv_idx = attack_idx & (np.random.rand(len(df)) < 0.3)  # 30% of attacks become adversarial
    # Controlled adversarial pattern: mimic normal traffic but keep label as attack
    # Use mean/median of normal samples for adversarial attacks
    normal_df = df[df['is_anomaly'] == 0]
    for col in ['src_ip', 'dst_ip', 'payload_size', 'duration']:
        median_val = normal_df[col].median()
        df.loc[adv_idx, col] = median_val + np.random.normal(0, 0.05 * normal_df[col].std(), adv_idx.sum())
    # Protocol: randomly pick from normal protocols
    normal_protocols = normal_df['protocol'].unique()
    df.loc[adv_idx, 'protocol'] = np.random.choice(normal_protocols, adv_idx.sum())

    X = df[['src_ip', 'dst_ip', 'protocol', 'port', 'payload_size', 'duration']]
    y = df['is_anomaly'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.25, random_state=42
    )

    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("\n[ℹ️] Label Distribution:")
    print("Ground Truth :", Counter(y_test))
    print("Predictions  :", Counter(y_pred))


    print("\n[📊] Classification Report:")
    report = classification_report(y_test, y_pred, output_dict=True, digits=4)
    print(classification_report(y_test, y_pred, digits=4))

    # Print macro avg and weighted avg as percentages
    macro_avg = report['macro avg']
    weighted_avg = report['weighted avg']
    print("\n[✅] Macro avg:")
    print(f"Precision: {macro_avg['precision']*100:.2f}  Recall: {macro_avg['recall']*100:.2f}  F1-score: {macro_avg['f1-score']*100:.2f}")
    print("[✅] Weighted avg:")
    print(f"Precision: {weighted_avg['precision']*100:.2f}  Recall: {weighted_avg['recall']*100:.2f}  F1-score: {weighted_avg['f1-score']*100:.2f}")

if __name__ == "__main__":
    main()
