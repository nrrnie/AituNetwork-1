from requests.exceptions import RequestException
from requests import post
from os import getenv


class API:
    def __init__(self):
        self.host = getenv('API_host')

    def find_user_by_id(self, user_id: int) -> dict:
        link = self.host + '/users/user_by_id/%d' % user_id
        response = API.safe_request(link)
        return response if response['status'] == 'error' else response['response']

    def find_user_by_barcode(self, barcode: int) -> dict:
        link = self.host + '/users/user_by_barcode/%d' % barcode
        response = API.safe_request(link)
        return response if response['status'] == 'error' else response['response']
        
    def login(self, barcode: int, password: str) -> dict:
        link = self.host + '/auth/login'
        data = dict(barcode=barcode, password=password)
        response = API.safe_request(link, data=data)
        return response if response['status'] == 'error' else response['response']
        
    def add_user(self, barcode: int, first_name: str, last_name: str, password: str):
        link = self.host + '/auth/add/user'
        data = dict(barcode=barcode, first_name=first_name, last_name=last_name, password=password)
        response = API.safe_request(link, data=data)
        return response if response['status'] == 'error' else response['response']

    @staticmethod
    def safe_request(link: str, data: dict = None) -> dict:
        try:
            response = post(link, data=data).json()
        except RequestException:
            return {'status': 'error', 'error': 'API error'}

        return {'status': 'ok', 'response': response}
