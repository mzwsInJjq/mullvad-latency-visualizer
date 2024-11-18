import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Seaborn theme
sns.set_theme(style="darkgrid")

# Step 1: Read the CSV file
df = pd.read_csv('us_ca_relays.csv')

# Step 2: Clean the data
# Remove rows where avg_ping is 'Failed'
df = df[df['avg_ping'] != 'Failed']
# Convert avg_ping to numeric
df['avg_ping'] = pd.to_numeric(df['avg_ping'])

# Step 3: Extract city information from the relay names
df['City'] = df['hostname'].apply(lambda x: x.split('-')[1].upper())

# Step 4: Define 22 distinct custom colors (reshuffled)
custom_colors = [
    '#d62728', '#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173', '#5254a3', '#6b6ecf', '#9c9ede', '#8ca252', '#b5cf6b',
    '#bd9e39', '#ad494a'
]

# Step 5: Plot the data
plt.figure(figsize=(5.5, 10))
sns.scatterplot(data=df, y='City', x='avg_ping', hue='City', palette=custom_colors, legend=False)
plt.rcParams['font.family'] = 'DejaVu Sans'

# Make city names boldface
for text in plt.gca().get_yticklabels():
    text.set_fontweight('bold')

for city in df['City'].unique():
    city_data = df[df['City'] == city]
    min_latency = city_data['avg_ping'].min()
    max_latency = city_data['avg_ping'].max()
    min_latency_row = city_data[city_data['avg_ping'] == min_latency]
    max_latency_row = city_data[city_data['avg_ping'] == max_latency]
    plt.annotate(min_latency, (min_latency_row['avg_ping'].values[0], min_latency_row['City'].values[0]),
                 textcoords="offset points", xytext=(2,1.6), ha='right', color='blue', fontsize=8)
    plt.annotate(max_latency, (max_latency_row['avg_ping'].values[0], max_latency_row['City'].values[0]),
                 textcoords="offset points", xytext=(-2,1.6), ha='left', color='red', fontsize=8)

plt.title('Mullvad US and CA Relays Latency')
plt.ylabel('')
plt.xlabel('ms')
plt.tight_layout()
plt.savefig('us_ca_relays.png', dpi=600)