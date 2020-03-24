import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
import json
import pandas as pd
import copy
from sklearn.metrics import classification_report


def intent_detection(project_id, session_id, credentials_file_path, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    try:

        credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
        session_client = dialogflow.SessionsClient(credentials=credentials)

        session = session_client.session_path(project_id, session_id)
        print('Session path: {}\n'.format(session))

        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))

        prediction = response.query_result.intent.display_name

        if prediction == 'Default Fallback Intent':
            prediction = 'None'

    except:

        prediction = 'Fail'

    return prediction


def create_json_intent_files(knowledge_base, language):

    path_intents = './New_agent/intents/'

    with open('./Dialogflow_templates/intent_template/Intent_template_usersays.json') as file:
        intent_usersays_template = json.load(file)

    with open('./Dialogflow_templates/intent_template/Intent_response_template.json') as file:
        intent_responses_template = json.load(file)

    with open('./Dialogflow_templates/agent_template.json') as file:
        agent_template = json.load(file)

    for intent in knowledge_base['intent'].unique():

        intent_utterances = []
        intent_data = knowledge_base.loc[knowledge_base['intent'] == intent]

        for utterance in intent_data['utterance']:

            data = copy.deepcopy(intent_usersays_template[0])
            data['data'][0]['text'] = utterance
            intent_utterances.append(data)

        with open(path_intents + intent + '_usersays_'+language+'.json', 'w') as fp:
            json.dump(intent_utterances, fp)

        intent_responses = copy.deepcopy(intent_responses_template)
        intent_responses['name'] = intent
        intent_responses['responses'][0]['messages'][0]['lang'] = language
        intent_responses['responses'][0]['messages'][0]['speech'] = 'Respuesta 1 ' + intent

        with open(path_intents + intent + '.json', 'w') as fp:
            json.dump(intent_responses, fp)

    agent_template['language'] = language

    with open('./New_agent/agent.json', 'w') as fp:
        json.dump(agent_template, fp)

    return print('======= JSON intent files have been created ======')


def performance_measures_report(knowledgebase, excel_name):

    metrics_per_intent = classification_report(knowledgebase['intent'], knowledgebase['prediction'],
                                               output_dict=True)

    df_metrics = pd.DataFrame.from_dict(metrics_per_intent, orient='index')
    global_metrics = df_metrics.loc[['macro avg', 'micro avg', 'weighted avg']]
    df_metrics = df_metrics.drop(['macro avg', 'micro avg', 'weighted avg']).sort_values(by=['f1-score'], ascending=False)

    errors_idx = knowledgebase['prediction'] != knowledgebase['intent']

    fail_utterances = pd.concat([knowledgebase['utterance'][errors_idx],
                                knowledgebase['intent'][errors_idx],
                                knowledgebase['prediction'][errors_idx]],
                                axis=1, keys=['utterance', 'real', 'predicted'])

    writer = pd.ExcelWriter(excel_name + '.xlsx', engine='xlsxwriter')
    df_metrics.to_excel(writer, sheet_name='results_per_intent')
    global_metrics.to_excel(writer, sheet_name='general_result')
    fail_utterances.to_excel(writer, sheet_name='fail_utterances',index=False)
    writer.save()

    print('============== The performance measures have been saved ==============')


