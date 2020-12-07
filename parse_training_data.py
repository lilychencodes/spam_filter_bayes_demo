import csv
import sys
import string

csv.field_size_limit(sys.maxsize)


class EmailCSVParser:
    def __init__(self):
        self.spam = 0
        self.ham = 0
        self.unique_words = {}  # e.g. {'hello': 4, ... }
        self.total_spam_words = 0
        self.total_ham_words = 0
        self.spam_words = {}  # e.g. {'hello': 4, ... }
        self.ham_words = {}  # e.g. {'hello': 5, ...}

    def tally(self, is_spam, row):
        for message in row:
            # lowercase all letters
            m = message.lower()
            # remove punctuations
            m = m.translate(str.maketrans('', '', string.punctuation))
            # remove numbers
            m = m.translate(str.maketrans('', '', string.digits))
            words = m.split()
            for word in words:
                if self.unique_words.get(word):
                    self.unique_words[word] += 1
                else:
                    self.unique_words[word] = 1

                if is_spam:
                    self.total_spam_words += 1
                    if self.spam_words.get(word):
                        self.spam_words[word] += 1
                    else:
                        self.spam_words[word] = 1
                else:
                    self.total_ham_words += 1
                    if self.ham_words.get(word):
                        self.ham_words[word] += 1
                    else:
                        self.ham_words[word] = 1

    def parse(self, training_data):
        with open(training_data, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            currently_reading_spam = None
            for i, row in enumerate(reader):
                if (i == 0):
                    # first row is the label of each column; so skip
                    continue

                # email text can contain multiple lines. If line doesn't start with an integer followed by either "ham" or "spam", then it's not a new email
                first_val_is_integer = False

                try:
                    first_val_is_integer = int(row[0])
                    first_val_is_integer = True
                except:
                    pass
                second_val_is_ham_or_spam = False
                try:
                    if row[1] == 'ham' or row[1] == 'spam':
                        second_val_is_ham_or_spam = True
                except IndexError:
                    pass

                is_new_email = first_val_is_integer and second_val_is_ham_or_spam
                if is_new_email:
                    is_spam = row[1] == 'spam'
                    currently_reading_spam = True if is_spam else False

                    # increment number of spam or non spam by 1
                    if is_spam:
                        self.spam += 1
                    else:
                        self.ham += 1

                    self.tally(currently_reading_spam, row[2:])
                else:
                    self.tally(currently_reading_spam, row)

        return {
            'spam': self.spam,
            'ham': self.ham,
            'unique_words': self.unique_words,
            'total_spam_words': self.total_spam_words,
            'total_ham_words': self.total_ham_words,
            'spam_words': self.spam_words,
            'ham_words': self.ham_words,
        }
