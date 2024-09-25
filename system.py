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
import heapq

# Function to calculate Jaccard similarity
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)  # Count of intersection
    union = len(set1 | set2)          # Count of union
    return intersection / union if union else 0

# Load answers into a list of tuples (doc_id, answer_tokens)
with open('answers.tsv', newline='') as answers, open('topics_1.tsv', newline='') as topics1, open('topics_2.tsv', newline='') as topics2:
    answer_reader = csv.reader(answers, delimiter='\t')
    topic_reader1 = csv.reader(topics1, delimiter='\t')
    topic_reader2 = csv.reader(topics2, delimiter='\t')

    # Preprocess answers
    answers_list = [(doc[0], set(doc[1].split())) for doc in answer_reader]

    # Dictionary to store the top 100 results for each query
    top_100_results1 = {}
    top_100_results2 = {}

    # Iterate through each query
    for query in topic_reader1:
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
        top_100_results1[query_id] = {doc_id: score for doc_id, score in top_100}
    
    for query in topic_reader2:
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
        top_100_results2[query_id] = {doc_id: score for doc_id, score in top_100}

# Example of how to access the results:

with open('result_binary_1.tsv', 'w', newline='') as binarytsv1:
    binary_writer1 = csv.writer(binarytsv1, delimiter='\t')
    for query_id, answers in top_100_results1.items():
        rank = 1
    # Iterate over the inner dictionary (answer IDs and scores)
        for answer_id, score in answers.items():
            binary_writer1.writerow([query_id, 'Q0', answer_id, rank, score, "binary1"])
            rank += 1

with open('result_binary_2.tsv', 'w', newline='') as binarytsv2:
    binary_writer2 = csv.writer(binarytsv2, delimiter='\t')
    for query_id, answers in top_100_results2.items():
        rank = 1
    # Iterate over the inner dictionary (answer IDs and scores)
        for answer_id, score in answers.items():
            binary_writer2.writerow([query_id, 'Q0', answer_id, rank, score, "binary2"])
            rank += 1
