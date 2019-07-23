import os, requests, time
from xml.etree import ElementTree

class TextToSpeech(object):
    def __init__(self, subscription_key, token_url, api_url):
        self.subscription_key = subscription_key
        self.token_url = token_url
        self.api_url = api_url
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.__get_token()

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def __get_token(self):
        fetch_token_url = self.token_url
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        try:
            response = requests.post(fetch_token_url, headers=headers)
            self.access_token = str(response.text)
            if self.access_token is not None:
                print('Retrieved access token')
        except Exception as e:
            print('Problem happened while getting access token:')
            print(e)

    def convert(self, text, save_location):
        print('Saving audio')
        base_url = self.api_url
        path = 'cognitiveservices/v1'
        user_agent = 'tts-api'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': user_agent
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.text = text
        body = ElementTree.tostring(xml_body)

        try:
            response = requests.post(constructed_url, headers=headers, data=body)
            '''
            If a success response is returned, then the binary audio is written
            to file in your working directory. It is prefaced by sample and
            includes the date.
            '''
            if response.status_code == 200:
                with open(save_location, 'wb') as audio_fp:
                    audio_fp.write(response.content)
                    print('\naudio clip saved successfully to {}'.format(save_location))
            else:
                print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        except Exception as e:
            print('Requests failed')
            print('Method: Post')
            print('URL: {}'.format(constructed_url))
            print('Headers: {}'.format(headers))
            raise(e)
