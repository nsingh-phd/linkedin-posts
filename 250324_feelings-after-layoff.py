import matplotlib.pyplot as plt
import numpy as np

# Feelings categories
feelings = [
    "WTH\n¯\\_(º_º)_/¯", "shocked", "glass\nhalf-empty",    # Negative
    "hopeful", "excited", "glass\nhalf-full"                # Positive
]

# Generate slightly uneven but roughly uniform values
np.random.seed(123456)
values = np.random.randint(8, 10, size=len(feelings))
error = np.random.uniform(0.1, 0.5, size=len(feelings))

# Define colors
colors = [
    "#E15759", "#EDC948", "#F28E2B", # Negative tones
    "#59A14F", "#4E79A7", "#FF9DA7"  # Positive tones
]

# Create bar plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(feelings, values, 
              yerr=error, capsize=5, 
              color=colors, edgecolor='black', linewidth=2)

# Add labels and title
ax.set_ylabel("intensity level", fontsize=12)
ax.set_title("feelings after the layoff", fontsize=20, fontweight="bold")
ax.set_ylim(0, max(values) + 1)

# Add website text in the top right corner
website_text = "https://n.singh.phd"
ax.text(5.6, max(values) + 0.5, 
        website_text, fontsize=10, color="gray", ha="right")

# Make it look more fun by tilting labels
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=10)

# adjust plot and remove extra spines
plt.subplots_adjust(bottom=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save plot
plt.savefig("plots/250324_feelings-after-layoff.png", dpi=300)

# Show plot
plt.show()
