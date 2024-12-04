import io
import pandas as pd
import matplotlib.pyplot as plt

# CSV-data as string
csv_data = """Frequency,18-25,26-35,36-45,46-55,56-65,65+
125,20,22,24,26,28,30
250,15,17,19,21,23,25
500,10,12,14,16,18,20
1000,5,7,9,11,13,15
2000,0,2,4,6,8,10
4000,-5,-3,1,5,10,15
8000,10,15,20,25,30,35
16000,60,65,70,75,80,85"""

# load CSV-data into a DataFrame
data = pd.read_csv(io.StringIO(csv_data), index_col='Frequency')

# creat plot
fig, ax = plt.subplots(figsize=(10, 6))

for column in data.columns:
    ax.plot(data.index, data[column], marker='o', label=column)

ax.set(title="Audiogram", ylabel="Audible amplitude range [dB]", xlabel="Frequency [Hz]")
ax.set_xscale('log')
ax.set_xticks(data.index)
ax.set_xticklabels(data.index)
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()
