import pandas as pd
import re  # For preprocessing raw text
from gensim.parsing.preprocessing import (
    strip_non_alphanum,
    strip_multiple_whitespaces,
    preprocess_string,
    split_alphanum,
    strip_short,
    strip_numeric,
)


#
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


#
def check_email(email):
    # read data from files
    p_non_spam = 0.0
    p_spam = 0.0
    parameters_non_spam = {}
    parameters_spam = {}

    # coef_values
    with open("coef_values.txt", "r") as f:
        data = f.read()
        values = data.split("\n")
        floats = list(map(float, values))
        p_spam = floats[0]
        p_non_spam = floats[1]

    # parameters_spam
    dataFrame_spam = pd.read_csv("parameters_spam.csv", header=None)
    parameters_spam = dict(dataFrame_spam.values)

    # parameters_not_spam
    dataFrame_non_spam = pd.read_csv("parameters_non_spam.csv", header=None)
    parameters_non_spam = dict(dataFrame_non_spam.values)

    email = extract_word_from_email(email).split()

    p_spam_given_email = p_spam
    p_non_spam_given_email = p_non_spam

    for word in email:
        if word in parameters_spam:
            p_spam_given_email *= parameters_spam[word]

        if word in parameters_non_spam:
            p_non_spam_given_email *= parameters_non_spam[word]

    print("P(Spam|email):", p_spam_given_email)
    print("P(Ham|email):", p_non_spam_given_email)

    if p_non_spam_given_email > p_spam_given_email:
        print("Това не е спам емайл")
    elif p_non_spam_given_email < p_spam_given_email:
        print("Това е спам емайл")
    else:
        print("Незнам трябва да проверя повече !")


def check_email_predicted(email):
    # read data from files
    p_non_spam = 0.0
    p_spam = 0.0
    parameters_non_spam = {}
    parameters_spam = {}

    # coef_values
    with open("coef_values.txt", "r") as f:
        data = f.read()
        values = data.split("\n")
        floats = list(map(float, values))
        p_spam = floats[0]
        p_non_spam = floats[1]

    # parameters_spam
    dataFrame_spam = pd.read_csv("parameters_spam.csv", header=None)
    parameters_spam = dict(dataFrame_spam.values)

    # parameters_not_spam
    dataFrame_non_spam = pd.read_csv("parameters_non_spam.csv", header=None)
    parameters_non_spam = dict(dataFrame_non_spam.values)

    email = extract_word_from_email(email).split()

    p_spam_given_email = p_spam
    p_non_spam_given_email = p_non_spam

    for word in email:
        if word in parameters_spam:
            p_spam_given_email *= parameters_spam[word]

        if word in parameters_non_spam:
            p_non_spam_given_email *= parameters_non_spam[word]

    if p_non_spam_given_email > p_spam_given_email:
        return 0
    elif p_non_spam_given_email < p_spam_given_email:
        return 1
    else:
        return "Unknown"
