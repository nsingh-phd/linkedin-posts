import matplotlib.pyplot as plt
import numpy as np

# Feelings categories
feelings = [
    "anger", "shock", "fear", "glass\nhalf-empty",      # Negative
    "relief", "hope", "excitement", "glass\nhalf-full"  # Positive
]

# Generate slightly uneven but roughly uniform values
np.random.seed(123456)
values = np.random.randint(8, 10, size=len(feelings))

# Define colors
colors = [
    "#E15759", "#EDC948", "#F28E2B", "#e76f51", # Negative tones
    "#59A14F", "#4E79A7", "#B07AA1", "#FF9DA7"  # Positive tones
]

# Create bar plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(feelings, values, color=colors, edgecolor='black', linewidth=2)

# Add labels and title
ax.set_ylabel("intensity level", fontsize=12)
ax.set_title("feelings after the layoff", fontsize=15, fontweight="bold")
ax.set_ylim(0, max(values) + 1)

# Add website text in the top right corner
website_text = "https://n.singh.phd"
ax.text(7.5, max(values) + 0.25, 
        website_text, fontsize=10, color="black", ha="right")

# Make it look more fun by tilting labels
plt.xticks(rotation=30, fontsize=12)
plt.yticks(fontsize=10)

# Save plot
plt.subplots_adjust(bottom=0.2)
plt.savefig("plots/250324_feelings-after-layoff.png", dpi=300)

# Show plot
plt.show()
