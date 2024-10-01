# Information Retrieval Assignment 1

To run this assignment, open a folder containing the following files:
- preprocess.py
- system.py
- Answers.json
- topics_1.json
- topics_2.json

Next, run the preprocess.py file. This will clean the .json files and create
new .tsv files for the system.py file.

Once the preprocessing step has finished, the three new .tsv files should now
appear in your folder. These files are included in submission for convenience 
purposes.

Next, run the system.py file. This will run the entire search, and create two
new files: result_binary1.tsv and results_binary2.tsv. These can be passed
into your own evaluation measures to get results.