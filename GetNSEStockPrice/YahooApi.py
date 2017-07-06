"""
    Contains implementaion for Yahoo Finance Stock Syncer library
    inherits the ApiBase base class common to all API implementations
    License : GNU GPLv2
    Author : Rajaram Srinivasan
    Initial Commit : May 2016
"""
import sys
import json
from datetime import datetime
#from dateutil import tz
import requests
from ApiBase import ApiBase
class YahooApi(ApiBase):
    def __init__(self):
        """
            Initialising attributes specific to Google API
        """
        self.url_endpoint = 'http://finance.yahoo.com/webservice/v1/symbols/'
        self.batch_size = 25
        self.method = 'GET'

    def make_request(self, scrips):
        """
            See base class for documentation. Contains Yahoo specific implementation
            Warning : Throws exception. Use within try catch block
        """
        scrip_string = []
        for scrip in scrips:
            scrip_string.append(scrip+'.NS')
        url = self.url_endpoint+','.join(scrip_string)+'/quote?format=json'
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            print >> sys.stderr, 'YAHOO API ERROR'
            print >> sys.stderr, resp.json
            raise Exception('YAHOO API ERROR')
        return resp

    def process_response(self, text_responses):
        """
            See base class for documentation. Contains Yahoo specific implementation
            Warning : Throws exception. Use within try catch block
        """
        stock_data = {}
        for resp in text_responses:
            content = resp.text
            response = json.loads(content)
            resources = response['list']['resources']
            for resource in resources:
                price = resource['resource']['fields']['price']
                volume = resource['resource']['fields']['volume']
                scrip = resource['resource']['fields']['symbol'][:-3]
                timestamp_string = resource['resource']['fields']['utctime']
                timestamp = None
                temp_stock_dict = {'price':price,
                                   'volume':volume,
                                   'timestamp':timestamp}
                stock_data[scrip] = temp_stock_dict
        return stock_data
