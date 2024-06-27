import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV into a DataFrame
csv_file = "predictions\Llama-2-70b-hf\Llama-2-70b-hf_qa1_single-supporting-fact_train_Preds.csv"
df = pd.read_csv(csv_file)

# Assuming your CSV file has columns like 'Prompt', 'Prediction', 'Correct_Answer'
# Calculate length of narratives in terms of tokens (words)
df["Narrative_Length"] = df["Prompt"].apply(
    lambda x: len(x.split())
)  # assuming narratives are separated by spaces

# Define ranges for narrative length
ranges = [
    (0, 10),
    (10, 20),
    (20, 30),
    (30, 40),
    (40, float("inf")),
]  # adjust ranges as needed


# Function to categorize narrative length into defined ranges
def categorize_length(length):
    for i, (start, end) in enumerate(ranges):
        if start <= length < end:
            return f"{start}-{end-1} words"
    return f"{ranges[-1][0]}+ words"


# Apply the categorization function
df["Length_Range"] = df["Narrative_Length"].apply(categorize_length)

# Calculate accuracies within each range
accuracy_by_range = []

for range_label, group in df.groupby("Length_Range"):
    correct = (group["Prediction"] == group["Answer"]).sum()
    total = len(group)
    accuracy = correct / total
    accuracy_by_range.append({"Length_Range": range_label, "Accuracy": accuracy})

# Convert to DataFrame
accuracy_by_range = pd.DataFrame(accuracy_by_range)

# Sort by the ranges to ensure they are plotted in order
accuracy_by_range["Length_Range"] = pd.Categorical(
    accuracy_by_range["Length_Range"],
    categories=[f"{start}-{end-1} words" for start, end in ranges],
    ordered=True,
)
accuracy_by_range = accuracy_by_range.sort_values(by="Length_Range")

# Plotting accuracies by range
plt.figure(figsize=(10, 6))
sns.barplot(x="Length_Range", y="Accuracy", data=accuracy_by_range)
plt.title("Accuracy by Narrative Length Range")
plt.xlabel("Narrative Length Range")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.ylim(0, 1)  # Ensure y-axis starts from 0 and ends at 1 for accuracy
plt.grid(True)
plt.tight_layout()
plt.show()
