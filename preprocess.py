# Import needed libraries and download nltk data
import json
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re 
import string
nltk.download('punkt')
nltk.download('stopwords')

# leans text of stopwords and irrelevant punctuation 
def clean_text(text):

    cleaned = re.sub(r'<.*?>', '', text)
    cleaned = re.sub(r'[%s]' % re.escape(string.punctuation), '', cleaned)  # remove punctuation
    cleaned = re.sub(r'\d+', '', cleaned)  # remove digits
    cleaned = cleaned.lower().strip()
    stop_words = set(stopwords.words('english'))  # Set of English stop words
    word_tokens = word_tokenize(cleaned)  # Tokenize the text into words
    filtered_sentence = [word for word in word_tokens if word.lower() not in stop_words]
    
    return ' '.join(filtered_sentence)

# Read in 3 json files
with open('topics_1.json', 'r') as json_file1, open('topics_2.json', 'r') as json_file2, open('Answers.json', 'r') as json_file3:
    topics_data1 = json.load(json_file1)
    topics_data2 = json.load(json_file2)
    answers_data = json.load(json_file3)

# Open TSV files for writing
with open('topics_1.tsv', 'w', newline='') as tsv_file1, open('topics_2.tsv', 'w') as tsv_file2, open('Answers.tsv', 'w', newline='') as answers_file:
    tsv_writer1 = csv.writer(tsv_file1, delimiter='\t')
    tsv_writer2 = csv.writer(tsv_file2, delimiter='\t')
    answer_writer = csv.writer(answers_file, delimiter='\t')
    
    #Write to topics_1.tsv
    for topic in topics_data1:
        tsv_writer1.writerow([topic['Id'], clean_text(topic['Body'])])

    #Write to topics_2.tsv
    for topic in topics_data2:
        tsv_writer2.writerow([topic['Id'], clean_text(topic['Body'])])

    #Write to answers.tsv
    for answer in answers_data:
        answer_writer.writerow([answer['Id'], clean_text(answer['Text']), answer['Score']])