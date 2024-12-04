# Information Retrieval Assignment 2

To run this assignment, open a folder containing the following files:
- preprocess.py
- tfidfmodel.py
- bm25model.py
- Answers.json
- topics_1.json
- topics_2.json

Next, run the preprocess.py file. This will clean the .json files and create
new .tsv files for the system.py file.

Once the preprocessing step has finished, the three new .tsv files should now
appear in your folder. These files are included in submission for convenience 
purposes.

Next, run the tfidfmodel.py file. This will run the entire search, and create two
new files: result_tfidf_1.tsv and result_tfidf_2.tsv. These can be passed
into your own evaluation measures to get results.

Next, run the bm25model.py file. This will run the entire search, and create two
new files: result_bm25_1.tsv and result_bm25_2.tsv. These can be passed
into your own evaluation measures to get results.