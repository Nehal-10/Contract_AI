import pandas as pd

df = pd.read_csv(
    "data/training/contract_training_dataset.csv"
)

print(
    df["contract_type"].value_counts()
)