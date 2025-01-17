import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import pickle
import string
import spacy
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
import re


from sklearn.ensemble import *
from nltk.stem import WordNetLemmatizer 
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, auc, roc_curve
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split



#nltk.download('stopwords') 
#nltk.download('wordnet')
sns.set(style='whitegrid')

warnings.filterwarnings('ignore')

def clean_txt(docs):
    lemmatizer = WordNetLemmatizer() 
    # Correct mispelled words
    #spell = SpellChecker()
    #spellcorrection = [spell.correction(x) for x in docs]
    # split into words
    speech_words = nltk.word_tokenize(docs)
    # convert to lower case
    lower_text = [w.lower() for w in speech_words]
    # prepare regex for char filtering
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    # remove punctuation from each word
    stripped = [re_punc.sub('', w) for w in lower_text]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    words = [w for w in words if not w in  list(STOP_WORDS)]
    #Stemm all the words in the sentence
    lem_words = [lemmatizer.lemmatize(word) for word in words]
    combined_text = ' '.join(lem_words)
    return combined_text

def classification_metrics(model, y_test, y_pred):
    # print(f"Training Accuracy Score: {model.score(X_train, y_train) * 100:.1f}%")
    # print(f"Validation Accuracy Score: {model.score(X_test, y_test) * 100:.1f}%")
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    fig,ax = plt.subplots(figsize=(8,6))
    sns.heatmap(pd.DataFrame(conf_matrix), annot = True, cmap = 'YlGnBu',fmt = 'g')
    ax.xaxis.set_label_position('top')
    plt.tight_layout()
    plt.title('Confusion matrix for Logisitic Regression Model', fontsize=20, y=1.1)
    plt.ylabel('Actual label', fontsize=15)
    plt.xlabel('Predicted label', fontsize=15)
    plt.show()
    # print(classification_report(y_test, y_pred))

def save_model(model,filename):
    pickle.dump(model, open(filename, 'wb'))

df = pd.read_csv('overview-of-recordings.csv')
df_text = df[['phrase', 'prompt']]


df_text['phrase'] = df_text['phrase'].apply(clean_txt)


X = df['phrase']
y = df['prompt']

vec = TfidfVectorizer()

X = vec.fit_transform(X).toarray()


prompt = df_text["prompt"].unique()
prompt_dict = {value:index for index, value in enumerate(prompt)}
results = df_text["prompt"].map(prompt_dict)
# print(f'\n{prompt_dict}\n')


X_train, X_test, y_train, y_test = train_test_split(X, results, test_size=0.2, random_state=0)

text_clf = BaggingClassifier(n_estimators=10)
model = text_clf.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# classification_metrics(model, y_test, y_pred)

save_model(model, 'model.pkl')

save_model(vec, 'vectorizer.pkl')


def detectAilment(text):
    pred = [text]

    transform_vect =vec.transform(pred).toarray()
    if model.predict(transform_vect) == 0:
        return("Emotional pain")
    elif model.predict(transform_vect) == 1:
        return("Hair falling out")
    elif model.predict(transform_vect) == 2:
        return("Heart hurts")
    elif model.predict(transform_vect) == 3:
        return("Infected wound")
    elif model.predict(transform_vect) == 4:
        return("Foot achne")
    elif model.predict(transform_vect) == 5:
        return("Shoulder pain")
    elif model.predict(transform_vect) == 6:
        return("Injury from sports")
    elif model.predict(transform_vect) == 7:
        return("Skin issue")
    elif model.predict(transform_vect) == 8:
        return("Stomach ache")
    elif model.predict(transform_vect) == 9:
        return("Knee pain")
    elif model.predict(transform_vect) == 10:
        return("Joint pain")
    elif model.predict(transform_vect) == 11:
        return("Hard to breath")
    elif model.predict(transform_vect) == 12:
        return("Head ache")
    elif model.predict(transform_vect) == 13:
        return("Body feels weak")
    elif model.predict(transform_vect) == 14:
        return("Feeling Dizzy")
    elif model.predict(transform_vect) == 15:
        return("Back pain")
    elif model.predict(transform_vect) == 16:
        return("Open wound")
    elif model.predict(transform_vect) == 17:
        return("Internal pain")
    elif model.predict(transform_vect) == 18:
        return("Blurry vision")
    elif model.predict(transform_vect) == 19:
        return("Acne")
    elif model.predict(transform_vect) == 20:
        return("Muscle pain")
    elif model.predict(transform_vect) == 21:
        return("Neck pain")
    elif model.predict(transform_vect) == 22:
        return("Cough")
    elif model.predict(transform_vect) == 23:
        return("Ear ache")
        
    else:
        return("Feeling cold")
