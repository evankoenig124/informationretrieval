# Import needed libraries
import csv
import heapq

# Function to calculate similarity
def calculate_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0

# Load answers into a list of tuples
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
            sim = calculate_similarity(topic_tokens, answer_tokens)
            similarities.append((doc_id, sim))

        # Use a heap to find the top 100 results
        top_100 = heapq.nlargest(100, similarities, key=lambda x: x[1])
        
        # Store the top 100 results in a dictionary
        top_100_results1[query_id] = {doc_id: score for doc_id, score in top_100}
    
    # Iterate through each query
    for query in topic_reader2:
        query_id = query[0]
        topic_tokens = set(query[1].split())
        similarities = []

        # Calculate similarity for each answer
        for doc_id, answer_tokens in answers_list:
            sim = calculate_similarity(topic_tokens, answer_tokens)
            similarities.append((doc_id, sim))

        # Use a heap to find the top 100 results efficiently
        top_100 = heapq.nlargest(100, similarities, key=lambda x: x[1])
        
        # Store the top 100 results in a dictionary
        top_100_results2[query_id] = {doc_id: score for doc_id, score in top_100}

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