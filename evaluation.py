from ranx import Qrels, Run, evaluate

qrels = Qrels.from_file("qrel_1.tsv", kind="trec")
run = Run.from_file("result_binary_1.tsv", kind="trec")
print(evaluate(qrels, run, "precision@1"))
print(evaluate(qrels, run, "precision@5"))
print(evaluate(qrels, run, "ndcg@10"))
print(evaluate(qrels, run, "mrr"))
print(evaluate(qrels, run, "map"))
print(evaluate(qrels, run, "ndcg@10"))