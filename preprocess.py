'''
Pass in topic files to this file
Pass in only ID and title of each entry
Clean title to be list of keywords (Title - stopwords)
Pass in answers file to this file
Pass in ID of each entry
Clean title to be list of keywords (Title - stopwords)
Rewrite to TSV
'''
import json
import csv
import nltk
import re 
import string

def clean_text(text):

    cleaned = re.sub(r'<.*?>', '', text)
    cleaned = re.sub(r'[%s]' % re.escape(string.punctuation), '', cleaned)  # remove punctuation
    cleaned = re.sub(r'\d+', '', cleaned)  # remove digits
    cleaned = cleaned.lower().strip()


    
    return cleaned

with open('topics_1.json', 'r') as json_file:
    topics_data = json.load(json_file)

# Open a TSV file for writing
with open('topics_1.tsv', 'w', newline='') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    
    # Write the header (if needed)
    tsv_writer.writerow(['Id', 'Body'])
    
    # Write the data rows
    for topic in topics_data:
        tsv_writer.writerow([topic['Id'], clean_text(topic['Body'])])

# Load the JSON data
with open('Answers.json', 'r') as json_file:
    answers_data = json.load(json_file)

# Open a TSV file for writing
with open('Answers.tsv', 'w', newline='') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    
    # Write the header (if needed)
    tsv_writer.writerow(['ID', 'Text', 'Score'])
    
    # Write the data rows
    for answer in answers_data:
        tsv_writer.writerow([answer['Id'], clean_text(answer['Text']), answer['Score']])