class defect_managment_base_class():
    api = None

    def __init__(self):
        '''
            initialize api to the api wrapper object
        '''
        raise NotImplementedError

    def new_issue(self, **kwargs) -> dict:
        '''
        must be implemented in the sub classes
        :param kwargs: request json dict for the new issue method of the api
        :return: response json dict for the new issue method of the api
        '''
        raise NotImplementedError