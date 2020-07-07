## Conversational Assistant Based on Rasa

This project explains how to build a custom conversational assistant using RASA platform. 


### Prerequisites
You must have Rasa, NumPy, and Pandas installed.

### Project Structure

1. Corpus.xlsx - Knowledge base with intents and utterances examples.
2. create_rasa_files.py - It allows to create rasa files from excel files. 
3. models.py - This folder contains the trained nlu models.
4. data - This folder contains the nlu and stories data to train nlu model.

### Running the project

1. Clone Rasa project in a local directory.
```
git clone https://github.com/SebastianRestrepoA/training-conversational-agents.git
```

2. Create enviroment for run Rasa project. In your cloned folder run the following commands:
```
virtualenv env
env\Scripts\activate
pip install rasa
pip install pandas
pip install numpy
```

4. Run using below command to train nlu model.
```
rasa train
```

4. Run below command to start conversation with your assistant.
```
rasa shell
```
