import pandas as pd
from gensim.parsing.preprocessing import (
    strip_non_alphanum,
    strip_multiple_whitespaces,
    preprocess_string,
    split_alphanum,
    strip_short,
    strip_numeric,
)
import re  # For preprocessing raw text


def extract_word_from_email(email):
    # -------------- delete links
    email = re.sub(r"http\S+", "", email)
    email = re.sub(r"Subject:", "", email)
    # -------------- delete special characters and make the text to lowercase
    email = strip_non_alphanum(email).lower().strip()
    # -------------- split nonsense words (like b1,b2,a1,a2)
    email = split_alphanum(email)
    # -------------- delete alone characters(space,a ,b ,c, d ,1 ,2 ,3 ....)
    email = strip_short(email, minsize=2)
    return email


# get data from file "emails_short.csv"
email_spam = pd.read_csv("emails_short.csv", header=None, names=["Email", "Label"])


# reform data (remove links,special characrers,make text to lowercase...)
for index in email_spam.index:
    email_spam.loc[index, "Email"] = extract_word_from_email(
        email_spam.loc[index, "Email"]
    )

# get vocabulary with unique words
email_spam["Email"] = email_spam["Email"].str.split()

vocabulary = []
for email in email_spam["Email"]:
    for word in email:
        vocabulary.append(word)

vocabulary = list(set(vocabulary))

# count words
word_counts_per_email = {
    unique_word: [0] * len(email_spam["Email"]) for unique_word in vocabulary
}

for index, email in enumerate(email_spam["Email"]):
    for word in email:
        word_counts_per_email[word][index] += 1

word_counts = pd.DataFrame(word_counts_per_email)

training_set_clean = pd.concat([email_spam, word_counts], axis=1)

print(training_set_clean.head())


# Isolating spam and non_spam emails first
spam_emails = training_set_clean[training_set_clean["Label"] == 1]
non_spam_emails = training_set_clean[training_set_clean["Label"] == 0]

# P(Spam) and P(Non_Spam)
p_spam = len(spam_emails) / len(training_set_clean)
p_non_spam = len(non_spam_emails) / len(training_set_clean)

with open("coef_values.txt", "w") as file:
    # Write the two values to the file, separated by enter
    file.write(str(p_spam) + "\n" + str(p_non_spam))

# N_Spam
n_words_per_spam_email = spam_emails["Email"].apply(len)
n_spam = n_words_per_spam_email.sum()

# N_Non_Spam
n_words_per_non_spam_email = non_spam_emails["Email"].apply(len)
n_non_spam = n_words_per_non_spam_email.sum()

# N_Vocabulary
n_vocabulary = len(vocabulary)

# Laplace smoothing
alpha = 1

# Initiate parameters
parameters_spam = {unique_word: 0 for unique_word in vocabulary}

parameters_non_spam = {unique_word: 0 for unique_word in vocabulary}


# Calculate parameters
for word in vocabulary:
    n_word_given_spam = spam_emails[word].sum()  # spam_emails already defined
    p_word_given_spam = (n_word_given_spam + alpha) / (n_spam + alpha * n_vocabulary)
    parameters_spam[word] = p_word_given_spam
    n_word_given_non_spam = non_spam_emails[
        word
    ].sum()  # non_spam_emails already defined
    p_word_given_non_spam = (n_word_given_non_spam + alpha) / (
        n_non_spam + alpha * n_vocabulary
    )
    parameters_non_spam[word] = p_word_given_non_spam

with open("parameters_spam.csv", "w") as f:
    for key in parameters_spam.keys():
        f.write("%s,%s\n" % (key, parameters_spam[key]))

with open("parameters_non_spam.csv", "w") as f:
    for key in parameters_non_spam.keys():
        f.write("%s,%s\n" % (key, parameters_non_spam[key]))
