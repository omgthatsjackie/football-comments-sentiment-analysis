import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score


# Preprocessing the comment
def process(comment):
    # Tokenizing the comment
    tokens = word_tokenize(comment.lower())
    # Removing stopwords and punctuation characters
    cleaned_tokens = [token for token in tokens if token not in stop_words and token not in punctuation]
    letter_tokens = []
    # Removing all non-alphabetic characters
    for token in cleaned_tokens:
        token = ''.join([c for c in token if c.isalpha()])
        if token:
            letter_tokens.append(token)
    # Lemmatization of the comment
    lemmatized = [morph.parse(token)[0].normal_form for token in letter_tokens]
    return ' '.join(lemmatized)


df = pd.read_csv('labeled.csv')
comments = df['comment']
labels = df['toxic']
# x_train and y_train are used for training the model
# y_train and y_test are used for testing the model
x_train, x_test, y_train, y_test = train_test_split(comments, labels, test_size=0.25, random_state=42)
stop_words = set(stopwords.words('russian'))
morph = MorphAnalyzer()
# Vectorization by counting word frequencies
vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w[\w-]*\w\b")

x_train = [process(comment) for comment in x_train]
x_test = [process(comment) for comment in x_test]
x_train = vectorizer.fit_transform(x_train).toarray()
x_test = vectorizer.transform(x_test).toarray()

# Multinomial Naive Bayes classifier
model = MultinomialNB()
model.fit(x_train, y_train)
pred = model.predict(x_test)
acc = accuracy_score(y_test, pred)
f1 = f1_score(y_test, pred, average="micro")
print(f"Accuracy: {acc}, f1: {f1}")
