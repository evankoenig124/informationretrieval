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
from collections import defaultdict
import heapq
import time

start = time.time()

# Function to calculate Jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)  # Count of intersection
    union = len(set1 | set2)          # Count of union
    return intersection / union if union else 0

# Load answers into a list of tuples (doc_id, answer_tokens)
with open('answers.tsv', newline='') as answers, open('topics_1.tsv', newline='') as topics1:
    answer_reader = csv.reader(answers, delimiter='\t')
    topic_reader = csv.reader(topics1, delimiter='\t')

    # Preprocess answers
    answers_list = [(doc[0], set(doc[1].split())) for doc in answer_reader]

    # Dictionary to store the top 100 results for each query
    top_100_results = {}

    # Iterate through each query
    for query in topic_reader:
        query_id = query[0]
        topic_tokens = set(query[1].split())
        similarities = []

        # Calculate similarity for each answer
        for doc_id, answer_tokens in answers_list:
            sim = jaccard_similarity(topic_tokens, answer_tokens)
            similarities.append((doc_id, sim))

        # Use a heap to find the top 100 results efficiently
        top_100 = heapq.nlargest(100, similarities, key=lambda x: x[1])
        
        # Store the top 100 results in a dictionary
        top_100_results[query_id] = {doc_id: score for doc_id, score in top_100}

# Example of how to access the results:
print(top_100_results)
print(time.time()-start)