import math
from collections import defaultdict
import re
import csv
#Import needed libraries

#Reads TSV into dictionary for easier iteration
def read_tsv(file_path):
    dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            dict[row[0]] = row[1]
    return dict

#Simple specific tokenization
def tokenize(text):
    return re.findall(r'\w+', text.lower())

#Counts terms and adds terms 
def compute_tf(doc_tokens):
    tf = defaultdict(int)
    for token in doc_tokens:
        tf[token] += 1
    #Normalizing
    return {token: 1 + math.log(freq) for token, freq in tf.items()}

#Calculates IDF
def compute_idf(documents):
    idf = {}
    n = len(documents)
    df = defaultdict(int)
    for tokens in documents.values():
        unique_tokens = set(tokens)
        for token in unique_tokens:
            df[token] += 1

    #Normalizing
    for token, freq in df.items():
        idf[token] = math.log((n + 1) / (1 + freq)) + 1
 
    return idf


#Inverted index specifically for TFIDF
def build_inverted_index(documents, idf):
    inverted_index = defaultdict(dict)
    
    for doc_id, tokens in documents.items():
        tf = compute_tf(tokens)
        for token, freq in tf.items():
            tfidf = freq * idf[token]
            inverted_index[token][doc_id] = tfidf

    return inverted_index

#Rank documents based on TF-IDF
def rank_documents(query, inverted_index, idf, documents):
    query_tokens = tokenize(query)
    scores = defaultdict(float)
    
    for token in query_tokens:
        if token in inverted_index:
            idf_value = idf.get(token, 0)
            for doc_id, tfidf in inverted_index[token].items():
                scores[doc_id] += tfidf * idf_value
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]

#Connects all functions together
def tfidf(topics, answers, output, run):
    queriesdict = read_tsv(topics)
    answersdict = read_tsv(answers)
    answer_tokens = {doc_id: tokenize(text) for doc_id, text in answersdict.items()}
    idf = compute_idf(answer_tokens)
    inverted_index = build_inverted_index(answer_tokens, idf)

    with open(output, 'w', encoding='utf-8') as out:
        for query_id, query in queriesdict.items():
            ranked_docs = rank_documents(query, inverted_index, idf, answer_tokens)
            for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
                out.write(f"{query_id}\tQ0\t{doc_id}\t{rank}\t{score}\t{run}\n")

def main():
    queries_file1 = "topics_1.tsv"
    answers_file = "Answers.tsv"
    output_file1 = "result_tfidf_1.tsv"

    queries_file2 = "topics_2.tsv"
    output_file2 = "result_tfidf_2.tsv"

    tfidf(queries_file1, answers_file, output_file1, "tfidf-1")
    tfidf(queries_file2, answers_file, output_file2, "tfidf-2")
main()