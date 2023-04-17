import pandas as pd
from cscb705_main import *


emails_test_set = pd.read_csv(
    "emails_test_set.csv", header=None, names=["Email", "Label"]
)

emails_test_set["predicted"] = emails_test_set["Email"].apply(check_email_predicted)

print(emails_test_set)

# check accurary

correct = 0
total = emails_test_set.shape[0]

for row in emails_test_set.iterrows():
    row = row[1]
    if row["Label"] == row["predicted"]:
        correct += 1

print("Correct:", correct)
print("Incorrect:", total - correct)
print("Accuracy:", correct / total)
