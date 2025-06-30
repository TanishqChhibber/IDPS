import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

ACCURACY_LOG = "accuracy_log.csv"

fig, ax = plt.subplots()
plt.title("Live Detection Accuracy")
plt.xlabel("Time")
plt.ylabel("Accuracy (%)")


def animate(i):
    if not os.path.exists(ACCURACY_LOG):
        ax.clear()
        ax.text(0.5, 0.5, "accuracy_log.csv not found", ha='center', va='center', fontsize=12)
        plt.title("Live Detection Accuracy")
        plt.xlabel("Time")
        plt.ylabel("Accuracy (%)")
        plt.tight_layout()
        return
    df = pd.read_csv(ACCURACY_LOG)
    if df.empty or 'Timestamp' not in df.columns or 'Accuracy' not in df.columns:
        ax.clear()
        ax.text(0.5, 0.5, "Waiting for valid accuracy_log.csv...", ha='center', va='center', fontsize=12)
        plt.title("Live Detection Accuracy")
        plt.xlabel("Time")
        plt.ylabel("Accuracy (%)")
        plt.tight_layout()
        return
    ax.clear()
    ax.plot(df["Timestamp"], df["Accuracy"].astype(float), marker='o', color='b')
    plt.title("Live Detection Accuracy")
    plt.xlabel("Time")
    plt.ylabel("Accuracy (%)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=3000)  # Update every 3 seconds
plt.show()
