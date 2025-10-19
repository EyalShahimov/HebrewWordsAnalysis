from typing import List
from .roots_response import RootsResponse
from .conjugations_response import ConjugationsResponse
import requests
import json


# Website interaction class
class AcademyWebsite:
    def __init__(self, ajax_nonce: str):
        base_url = f'https://hebrew-academy.org.il/wp-admin/admin-ajax.php?_ajax_nonce={ajax_nonce}'
        self.__roots_url = f'{base_url}&action=get_shoresh_suggestions&prefix=%s'
        self.__conjugations_url = f'{base_url}&action=get_verb_conjugations&shoresh=%s&binyan=%s'

        # Standard headers to mimic a real browser
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        self.__expired_nonce_page = '-1'

    def fetch_roots(self, prefix: str) -> List[RootsResponse] | None:
        while True:
            response, success = self.__request(self.__roots_url % prefix)
            if not success:
                continue
            return [RootsResponse(**entry) for entry in response]


    def fetch_conjugations(self, root: str, stem: str) -> List[ConjugationsResponse] | None:
        while True:
            response, success = self.__request(self.__conjugations_url % (root, stem))
            if not success:
                continue
            return [ConjugationsResponse(**entry) for entry in response]

    def __request(self, url: str):
        page_text = requests.get(url, headers=self.__headers).text
        if page_text == self.__expired_nonce_page:
            raise Exception('Expired nonce')

        response = json.loads(page_text)
        if not response['success']:
            print(response)
            return response, False
        return response['data'], True