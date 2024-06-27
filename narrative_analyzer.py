import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from Excel into a DataFrame
excel_file = r"C:\Users\Josh\Documents\GitHub\bAbI_testing\predictions\Llama-2-70b-hf\Llama-2-70b-hf_qa2_two-supporting-facts_train_Preds.csv"
df = pd.read_excel(excel_file)

# Calculate length of narratives in terms of tokens (words)
df["narrative_length"] = df["prompt"].apply(
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
df["length_range"] = df["narrative_length"].apply(categorize_length)

# Calculate accuracy within each range
accuracy_by_range = df.groupby("length_range")["accuracy"].mean().reset_index()

# Sort by the ranges to ensure they are plotted in order
accuracy_by_range["length_range"] = pd.Categorical(
    accuracy_by_range["length_range"],
    categories=[f"{start}-{end-1} words" for start, end in ranges],
    ordered=True,
)
accuracy_by_range = accuracy_by_range.sort_values(by="length_range")

# Plotting accuracies by range
plt.figure(figsize=(10, 6))
sns.barplot(x="length_range", y="accuracy", data=accuracy_by_range)
plt.title("Accuracy by Narrative Length Range")
plt.xlabel("Narrative Length Range")
plt.ylabel("Accuracy")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
