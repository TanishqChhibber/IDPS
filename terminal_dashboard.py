# dashboard.py
import streamlit as st
import pandas as pd
import time
from collections import Counter

st.set_page_config(page_title="Live IDPS Dashboard", layout="wide")

st.title("🔍 Intrusion Detection & Prevention System Dashboard")
st.markdown("Real-time view of network traffic & detected anomalies.")

DATA_FILE = "idps_data.csv"


@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["src_ip", "dst_ip", "protocol", "is_anomaly"])

def get_classification_metrics(df):
    if len(df) == 0 or 'is_anomaly' not in df.columns:
        return None
    # Dummy y_pred = y_true for live view (replace with real predictions if available)
    y_true = df['is_anomaly']
    y_pred = df['is_anomaly']
    from sklearn.metrics import classification_report
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return report


# Streamlit autorefresh every 5 seconds
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="datarefresh")

df = load_data()
if not df.empty:
    st.subheader("📊 Anomaly Summary")
    count = Counter(df['is_anomaly'])
    st.metric("✅ Normal Traffic", count.get(0, 0))
    st.metric("🚨 Anomalies Detected", count.get(1, 0))

    st.subheader("📈 Recent Events")
    st.dataframe(df.tail(15).sort_index(ascending=False), use_container_width=True)

    st.subheader("📉 Protocol Distribution")
    st.bar_chart(df['protocol'].value_counts())

    # Classification report metrics
    st.subheader("📊 Classification Metrics (Live)")
    report = get_classification_metrics(df)
    if report:
        # Per-class metrics
        import pandas as pd
        metrics_df = pd.DataFrame({
            'precision': [report['0']['precision']*100, report['1']['precision']*100],
            'recall': [report['0']['recall']*100, report['1']['recall']*100],
            'f1-score': [report['0']['f1-score']*100, report['1']['f1-score']*100]
        }, index=['Normal (0)', 'Attack (1)'])
        st.bar_chart(metrics_df)

        # Macro/weighted avg
        avg_df = pd.DataFrame({
            'macro avg': [report['macro avg']['precision']*100, report['macro avg']['recall']*100, report['macro avg']['f1-score']*100],
            'weighted avg': [report['weighted avg']['precision']*100, report['weighted avg']['recall']*100, report['weighted avg']['f1-score']*100]
        }, index=['Precision', 'Recall', 'F1-score'])
        st.bar_chart(avg_df)

    # System resource usage
    import psutil
    st.subheader("🖥️ System Resource Usage (Live)")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    st.metric("CPU Usage (%)", cpu)
    st.metric("Memory Usage (%)", mem)
    st.progress(cpu/100, text="CPU Usage")
    st.progress(mem/100, text="Memory Usage")
