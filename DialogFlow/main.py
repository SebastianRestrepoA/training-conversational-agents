from dialogflow_functions import *
from sklearn.model_selection import train_test_split

knowledge_base_path = './KnowledgeBase.xlsx'
knowledge_base = pd.read_excel(knowledge_base_path)
y = knowledge_base["intent"]
x = knowledge_base["utterance"]

# Hold out method
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size=0.3)

training_knowledge_base = pd.concat((x_train, y_train), axis=1)

language = 'es'
create_json_intent_files(training_knowledge_base, language)


test_knowledge_base = pd.concat((x_test, y_test), axis=1)

project_id = 'dialogbot-268819'
session_id = '0123456789'
credentials_file_path = 'DialogBot-bf9ec707ce99.json'

# Evaluate our training
test_knowledge_base['prediction'] = test_knowledge_base['utterance'].apply(lambda utterance:
                                                                           intent_detection(project_id,
                                                                                            session_id,
                                                                                            credentials_file_path,
                                                                                            utterance, language))


performance_measures_report(test_knowledge_base, 'training_results')


