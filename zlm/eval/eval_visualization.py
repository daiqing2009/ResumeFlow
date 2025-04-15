import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = [
    ("Fine-tuned Gemma2_v2", "skill_section", 0.10, 0.884, 0.831, 0.855),
    ("Fine-tuned Gemma2_v2", "work_experience", 0.10, 0.863, 0.842, 0.852),
    ("Fine-tuned Gemma2_v3", "skill_section", 0.01, 0.904, 0.903, 0.903),
    ("Fine-tuned Gemma2_v3", "work_experience", 0.03, 0.884, 0.878, 0.881),
    ("Base Gemma2", "skill_section", 0.68, 0.904, 0.903, 0.903),
    ("Base Gemma2", "work_experience", 0.54, 0.880, 0.800, 0.838)
]

# Convert data to DataFrame
df = pd.DataFrame(data, columns=["Model", "Section", "Outlier Rate", "Precision", "Recall", "F1 Score"])

# Set plot style
sns.set_theme(style="whitegrid")

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
metrics = ["Outlier Rate", "Precision", "Recall", "F1 Score"]
colors = ["Blues", "Greens", "Oranges", "Purples"]

def plot_metric(ax, metric, palette):
    sns.barplot(x="Model", y=metric, hue="Section", data=df, ax=ax, palette=palette)
    ax.set_title(f"{metric} by Model")
    ax.set_xlabel("Model")
    ax.set_ylabel(metric)
    ax.legend(title="Section")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f")

# Plot each metric
for ax, metric, palette in zip(axes.flatten(), metrics, colors):
    plot_metric(ax, metric, palette)

plt.tight_layout()
plt.show()
