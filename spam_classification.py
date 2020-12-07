import string
import math

from parse_training_data import EmailCSVParser

# Note: this is not the most elegant or optimized piece of code.
# However, I purposefully sacrified elegance for readability since this is
# a demo of beginner's intro to machine learning series.
# Link to article here: https://medium.com/@lilychencodes/understanding-and-implementing-machine-learning-algorithm-for-spam-filter-a508fb9547bd


class SpamClassification:
    def __init__(self, training_data):
        # e.g. 'spam_ham_dataset.csv'
        self.training_data = training_data
        self.spam = 0
        self.ham = 0
        self.unique_words = {}  # e.g. {'hello': 4, ... }
        self.total_spam_words = 0
        self.total_ham_words = 0
        self.spam_words = {}  # e.g. {'hello': 4, ... }
        self.ham_words = {}  # e.g. {'hello': 5, ...}

        # train with given training_data to set properties
        self.train()

    def train(self):
        parser = EmailCSVParser()
        result = parser.parse(self.training_data)
        print('Finished training with data from', self.training_data)
        self.spam = result.get('spam')
        self.ham = result.get('ham')
        self.unique_words = result.get('unique_words')
        self.total_spam_words = result.get('total_spam_words')
        self.total_ham_words = result.get('total_ham_words')
        self.spam_words = result.get('spam_words')
        self.ham_words = result.get('ham_words')

    def log_p_words_given_spam(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())
        for word in email:
            # how many times word appears in spam emails plus 1
            nominator = (self.spam_words.get(word) or 0) + 1
            # num total words in spam emails + num unique words in training set
            denominator = self.total_spam_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def log_p_words_given_ham(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())
        for word in email:
            # how many times word appears in non spam emails plus 1
            nominator = (self.ham_words.get(word) or 0) + 1
            # num total words in non spam emails + num unique words in training set
            denominator = self.total_ham_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def clean(self, email):
        file = open(email, 'r')
        lines = file.readlines()

        all_words = []

        for line in lines:
            # lowercase all letters
            m = line.lower()
            # remove punctuations
            m = m.translate(str.maketrans('', '', string.punctuation))
            # remove numbers
            m = m.translate(str.maketrans('', '', string.digits))
            words = m.split()
            all_words += words

        return all_words

    # This is the method to call to classify an email. From terminal, run:
    # >>> from spam_classification import SpamClassification
    # >>> c = SpamClassification('spam_ham_dataset.csv')
    # >>> c.classify('bay_to_breakers.txt')
    def classify(self, email):
        cleaned_email = self.clean(email)
        # print('email words:', cleaned_email)
        log_p_spam = math.log(self.spam / (self.spam + self.ham))
        log_p_ham = math.log(self.ham / (self.spam + self.ham))
        log_p_words_given_spam = self.log_p_words_given_spam(cleaned_email)
        log_p_words_given_ham = self.log_p_words_given_ham(cleaned_email)
        log_probability_of_spam = log_p_spam + log_p_words_given_spam
        log_probability_of_ham = log_p_ham + log_p_words_given_ham
        # print('log_p_spam: ', log_p_spam)
        # print('log_p_ham: ', log_p_ham)
        # print('log_p_words_given_spam: ', log_p_words_given_spam)
        # print('log_p_words_given_ham: ', log_p_words_given_ham)
        return log_probability_of_spam > log_probability_of_ham
