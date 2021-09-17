import json
import requests

class DataGenService:
    #base_url = 'http://localhost:8080'
    base_url = 'http://datagen_server:8080'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def __init__(self):
        pass

    def getAllData(self):
        url = self.base_url + "/data"
        response = requests.get(url).json()
        return response

    def getLabels(self):
        return requests.get(self.base_url + '/data/labels', headers=self.headers).text

    def getDataTypes(self):
        return requests.get(self.base_url + '/data/types', headers=self.headers).text

    def getDataById(self, dataId):
        '''

        :param dataId:
        :return:
        '''
        url = self.base_url + "/data/" + str(dataId)
        response = requests.get(url, headers=self.headers).json()
        return response

    def getValueByName(self, name, *labels):
        '''

        :param name:
        :param labels:
        :return:
        '''
        url = self.base_url + "/value/" + str(name)
        if labels is not None:
            list(labels).sort()
        response = requests.get(url, params={'labels': labels}, headers=self.headers).text
        return response

    def getDataByName(self, name, *labels):
        '''

        :param name:
        :param labels:
        :return:
        '''
        url = self.base_url + "/data/" + str(name)
        if labels is not None:
            list(labels).sort()
        response = requests.get(url, headers=self.headers).json()
        return response

    def getAllNames(self):
        '''

        :return:
        '''
        pass

    def newData(self, json_data):
        url = self.base_url + "/data"
        headers = {"Content-Type": "application/json"};
        response = requests.post(url, json=json_data, headers=headers)
        return response

    def buildNewData(self, name, value, dataType="STATIC", onTimeUse=False, *labels, **properties):
        dataTypes = self.getDataTypes()
        data = {'name': str(name),
                'value': str(value),
                'dataType': str(dataType).upper(),
                'onTimeUse': bool(onTimeUse),
                'labels': [],
                'properties': {}
                }
        if labels is not None:
            for l in labels:
                data['labels'] += labels
        if properties is not None:
            data['properties'] = properties
        return data

    # TODO: handle http errors
    # TODO: create the remaining patch and put
    # TODO: create the user input loop in the main
    # TODO: document all methods
    # TODO: package and deploy
