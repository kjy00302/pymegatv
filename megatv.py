# -*- coding: utf-8 -*-

import requests
import uuid


class Megatv():
    request_headers = {
        'requestHostname': 'otmapp',
        'User-Agent': 'OMS (compatible;ServiceType/OTM;DeviceType/WIN8PAD;DeviceModel/G41TM6;OSType/WINM;OSVersion/8.1.0;AppVersion/1.2.1.1)'
        }
    applicationKey = 'IG9RIXFXD24R1DS2LRSD1HKLD8QQZKL6'

    def __init__(self):
        self.websession = requests.Session()
        self.userinfo = None
        self.uuid = uuid.uuid4().hex
        self.session_id = None

    def login(self, username, password, raw=False):
        userinfo = self.websession.post('https://omas.megatvdnp.co.kr/login/olleh', json={'userId': username, 'userPwd': password}, headers={'applicationKey': self.applicationKey, 'transactionId': '0', 'timestamp': '', 'requestHostname': 'otmapp'}).json()
        if raw:
            return userinfo

        if userinfo.get('systemMessage') == u'로그인에 성공하였습니다.':
            self.userinfo = userinfo
            return True

        else:
            return False

    def login_token(self, token, raw=False):
        userinfo = self.websession.post('https://omas.megatvdnp.co.kr/login/auto', json={'toknVal': token}, headers={'applicationKey': self.applicationKey, 'transactionId': '0', 'timestamp': '', 'requestHostname': 'otmapp'}).json()

        if raw:
            return userinfo

        if userinfo.get('systemMessage') == u'로그인에 성공하였습니다.':
            self.userinfo = userinfo
            return True

        else:
            return False

    def session_create(self, raw=False):
        session = self.websession.post('http://contents.megatvdnp.co.kr/app5/0/API/create_session.aspx', headers=self.request_headers, params={'uuid': self.uuid}).json()

        if raw:
            return session

        if session.get('meta').get('code') == 200:
            self.session_id = session.get('data').get('session_id')
            return self.session_id
        else:
            return False

    def session_ready(self, raw=False):
        session = self.websession.post('http://contents.megatvdnp.co.kr/app5/0/API/ready_session.aspx', headers=self.request_headers, params={'uuid': self.uuid}).json()

        if raw:
            return session

        if session.get('meta').get('code') == 200:
            return True
        else:
            return False

    def session_check(self, session_id=None, raw=False):
        if session_id is None:
            session_id = self.session_id

        session = self.websession.post('http://contents.megatvdnp.co.kr/app5/0/API/check_session.aspx', headers=self.request_headers, params={'uuid': self.uuid, 'session_id': session_id}).json()

        if raw:
            return session

        if session.get('meta').get('code') == 200:
            return True
        else:
            return False
 
    def session_delete(self, session_id=None, raw=False):
        if session_id is None:
            session_id = self.session_id

        session = self.websession.post('http://contents.megatvdnp.co.kr/app5/0/API/delete_session.aspx', headers=self.request_headers, params={'uuid': self.uuid, 'session_id': session_id}).json()

        if raw:
            return session

        if session.get('meta').get('code') == 200:
            self.session_id = None
            return True
        else:
            return False

    def get_channels(self, test=False, raw=False):
        if test:
            test = 1
        else:
            test = 0

        channels = self.websession.get('http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_chlist', params={'category_id': 1, 'istest': test}, headers=self.request_headers).json()

        if raw:
            return channels

        if channels.get('meta').get('code') == '200':
            return channels.get('data').get('list')[0].get('list_channel')
        else:
            return None

    def get_my_channels(self, test=False, raw=False):
        if test:
            test = 1
        else:
            test = 0

        channels = self.websession.get('http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_chlist', params={'category_id': 1, 'istest': test}, headers=self.request_headers).json()

        if raw:
            return channels

        if channels.get('meta').get('code') == '200':
            return channels.get('data').get('list')[0].get('list_my_channel')
        else:
            return None

    def get_epg(self, ch_no, test=False, raw=False):
        if test:
            test = 1
        else:
            test = 0
        epgdata = self.websession.get('http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_proglist', params={'ch_no': ch_no, 'istest': test}, headers=self.request_headers).json()

        if raw:
            return epgdata

        if epgdata.get('meta').get('code') == '200':
            return epgdata.get('data').get('list')
        else:
            return None

    def get_channel_url(self, ch_no, bit_rate, raw=False):
        request_query = {
            'istest': 0,
            'ch_no': ch_no,
            'bit_rate': 'S',
            'bit_rate_option': bit_rate,
            'user_model': 'G41TM6',
            'user_os': 'Win10.0',
            'user_type': 'Computer.Desktop',
            'user_net': 'WIFI'
            }
        urlinfo = self.websession.get('http://menu.megatvdnp.co.kr:38080/app5/0/api/epg_play', headers=self.request_headers, params=request_query).json()
 
        if raw:
            return urlinfo

        if urlinfo.get('meta').get('code') == '200':
            return urlinfo.get('data')
        else:
            return None
