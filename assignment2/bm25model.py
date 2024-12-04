import math
import re
import csv
from collections import defaultdict
#Import needed libraries

# Parameters for BM25, tuned for performance
k1 = 1.5
b = 0.75

#finds TF from specific term
def calculate_tf(term, document):
    return document.count(term)

#Finds single idf (bm25)
def calculate_idf(term, num_docs, doc_freq):
    return math.log((num_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1)

#Reads TSV into dictionary for easier iteration
def read_tsv(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data[row[0]] = row[1]
    return data

#Simple specific tokenization
def tokenize(text):
    return re.findall(r'\w+', text.lower())

# Build inverted index specifically for BM25
def build_inverted_index(answers):
    inverted_index = defaultdict(lambda: defaultdict(int))
    doc_lengths = {}
    total_length = 0

    for doc_id, content in answers.items():
        words = content.split()
        doc_lengths[doc_id] = len(words)
        total_length += len(words)
        unique_words = set(words)

        for word in unique_words:
            inverted_index[word][doc_id] = calculate_tf(word, words)

    avg_doc_length = total_length / len(answers)
    return inverted_index, doc_lengths, avg_doc_length

#Rank Docs
def bm25_score(query, inverted_index, doc_lengths, avg_doc_length, num_docs):
    scores = defaultdict(float)
    query_terms = query.split()

    for term in query_terms:
        if term in inverted_index:
            doc_freq = len(inverted_index[term])
            idf = calculate_idf(term, num_docs, doc_freq)

            for doc_id, tf in inverted_index[term].items():
                doc_len = doc_lengths[doc_id]
                score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_length))))
                scores[doc_id] += score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]
    return sorted_scores

#Connects everything together
def bm25(topics, answers, output_file, run):
    queriesdict = read_tsv(topics)
    answersdict = read_tsv(answers)
    inverted_index, doc_lengths, avg_doc_length = build_inverted_index(answersdict)
    num_docs = len(answersdict)

    with open(output_file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        for query_id, query in queriesdict.items():
            top_results = bm25_score(query, inverted_index, doc_lengths, avg_doc_length, num_docs)
            for rank, (doc_id, score) in enumerate(top_results):
                writer.writerow([query_id,"Q0", doc_id, rank + 1, score, run])

def main():
    queries_file1 = 'topics_1.tsv'
    answers_file = 'Answers.tsv'
    output_file1 = 'result_bm25_1.tsv'

    queries_file2 = 'topics_2.tsv'
    output_file2 = 'result_bm25_2.tsv'

    bm25(queries_file1, answers_file, output_file1, "bm25-1")
    bm25(queries_file2, answers_file, output_file2, "bm25-2")
main()