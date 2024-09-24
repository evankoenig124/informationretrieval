'''
Takes cleaned jsons (now TSV)
Finds ratio of keywords in topics to answers 
Write that value to score
qID is the query (topic) ID
Q0 is the literal Q0 (Just simply print Q0)
answerID is the ID of an answer returned for qID
rank (1-100) is the rank of this answer for this qID
score is a system similarity score indicating of the quality of the answer to the query
runName is the identifier for the system (any string)
after score is calculated by ratios, rank them by score and write value to rank
'''
import csv

for filenum in range(1, 3):
    with open('answers.tsv', newline='') as answers, open(f'topics_{filenum}.tsv', newline='') as topics:
        tsv_reader1 = csv.reader(answers, delimiter='\t')
        tsv_reader2 = csv.reader(topics, delimiter='\t')