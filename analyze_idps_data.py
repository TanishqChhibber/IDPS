import pandas as pd

# Load the data
df = pd.read_csv('idps_data.csv')

# Class balance
print('Class distribution:')
print(df['is_anomaly'].value_counts())
print('\nPercentage of attacks (is_anomaly=1): {:.2f}%'.format(100 * df['is_anomaly'].sum() / len(df)))

# Check if dst_ip or protocol is a strong indicator of attack
print('\nAttack destination IPs:')
print(df[df['is_anomaly'] == 1]['dst_ip'].value_counts().head(10))

print('\nAttack protocols:')
print(df[df['is_anomaly'] == 1]['protocol'].value_counts())

print('\nNormal destination IPs:')
print(df[df['is_anomaly'] == 0]['dst_ip'].value_counts().head(10))

print('\nNormal protocols:')
print(df[df['is_anomaly'] == 0]['protocol'].value_counts())
