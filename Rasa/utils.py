import pandas as pd
import requests
import unicodedata
from sklearn.metrics import classification_report


def convert_excel_to_md(path, create_files_path, nlu_file=True, stories_file=True, domain_file=True):
    """
    Converts an excel file created with the specified format to RASA accepted nlu.md format
    :param path: path where the excel file is saved
    :param create_files_path: path where the nlu.md file needs to be created
    :return: return nothing. A file is created in the path specified via create_files_path
    """
    df = pd.read_excel(path)
    intent_names = list(set(df['intent']))

    if nlu_file is True:

        file = open(r'{}\data\nlu.md'.format(create_files_path), "w")

        for intent_name in intent_names:
            file.write("## intent:{intent_name}\n".format(intent_name=intent_name))
            for utterance in df['utterance'][df['intent'] == intent_name].dropna():
                processed_utterance = remove_tilde(utterance)
                file.write("- {}\n".format(processed_utterance))
            file.write("\n")

        file.close()

    if stories_file is True:

        file = open(r'{}\data\stories.md'.format(create_files_path), "w")
        # file.write("## path 1\n")
        for intent_name in intent_names:
            file.write("## {intent_name} path\n".format(intent_name=intent_name))
            file.write("* {intent_name} \n".format(intent_name=intent_name))
            file.write("  - utter_{intent_name}\n".format(intent_name=intent_name))
            file.write("\n")

        file.close()

    if domain_file is True:

        file = open(r'{}\domain.yml'.format(create_files_path), "w")
        file.write("intents:\n")

        for intent_name in intent_names:
            file.write("  - {}\n".format(intent_name))

        file.write("\n")
        file.write("responses:\n")

        for intent_name in intent_names:
            file.write(" utter_{}:\n".format(intent_name))
            file.write("  - text: \"{}\"\n".format(intent_name))
            file.write("\n")

        file.close()

    print('============== The rasa files have been created ==============')


def remove_tilde(vUtterance):

    """ This function removes the accent mark (or "tilde") from a utterance.

    :param vUtterance: string variable with a utterance.

    :return: string variable with the utterance without "tildes".


    """

    if type(vUtterance) != str:
        print('no es un string: ' + str(vUtterance))

    return ''.join((c for c in unicodedata.normalize('NFD', vUtterance) if unicodedata.category(c) != 'Mn'))


def performance_measures_report(knowledgebase, excel_name):

    metrics_per_intent = classification_report(knowledgebase['intent'], knowledgebase['prediction'],
                                               output_dict=True)

    del metrics_per_intent['accuracy']

    df_metrics = pd.DataFrame.from_dict(metrics_per_intent, orient='index')
    global_metrics = df_metrics.loc[['macro avg', 'weighted avg']]
    df_metrics = df_metrics.drop(['macro avg', 'weighted avg']).sort_values(by=['f1-score'], ascending=False)

    errors_idx = knowledgebase['prediction'] != knowledgebase['intent']

    fail_utterances = pd.concat([knowledgebase['utterance'][errors_idx],
                                knowledgebase['intent'][errors_idx],
                                knowledgebase['prediction'][errors_idx]],
                                axis=1, keys=['utterance', 'real', 'predicted'])

    writer = pd.ExcelWriter(excel_name + '.xlsx', engine='xlsxwriter')
    df_metrics.to_excel(writer, sheet_name='results_per_intent')
    global_metrics.to_excel(writer, sheet_name='general_result')
    fail_utterances.to_excel(writer, sheet_name='fail_utterances', index=False)
    writer.save()

    print('============== The performance measures have been saved ==============')


def rasa_intent_detection(utterance):

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": 'Iam', "message": utterance})
    recognized_intent = r.json()[0]['text']
    print(recognized_intent)

    return recognized_intent
