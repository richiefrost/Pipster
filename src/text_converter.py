import os, requests, time
from xml.etree import ElementTree
import json

class TextToSpeech(object):
    def __init__(self, subscription_key, resource_region):
        self.subscription_key = subscription_key
        self.token_url = self.__get_token_url(resource_region)
        self.api_url = self.__get_api_url(resource_region)
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

    def __get_token_url(self, region):
        # TODO: Support more regions
        return 'https://westus2.api.cognitive.microsoft.com/sts/v1.0/issueToken'

    def __get_api_url(self, region):
        # TODO: Support more regions
        return "https://westus2.tts.speech.microsoft.com/cognitiveservices/v1"

    def convert(self, text, save_location):
        url = self.api_url
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-96kbitrate-mono-mp3',
            'User-Agent': 'tts-api'
        }

        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')

        voice_alias = "en-US-JessaNeural"
        voice.set('name', voice_alias) # Short name for 'Microsoft Server Speech Text to Speech Voice
        voice.text = text
        body = ElementTree.tostring(xml_body)

        try:
            response = requests.post(url, headers=headers, data=body)
            '''
            If a success response is returned, then the binary audio is written
            to file in your working directory. It is prefaced by sample and
            includes the date.
            '''
            if response.status_code == 200:
                with open(save_location, 'wb') as audio_fp:
                    audio_fp.write(response.content)
                    
                    # Need to save as mp3 so that iOS can play it
                    #_wav = AudioSegment.from_wav(save_location)
                    #_wav.export(save_location + '.mp3', format='mp3')

                    print('\naudio clip saved successfully to {}'.format(save_location))
            else:
                print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
        except Exception as e:
            print('Requests failed')
            print('Method: Post')
            print('URL: {}'.format(url))
            print('Headers: {}'.format(headers))
            raise(e)
            

if __name__ == '__main__':
    import sys
    import argparse

    with open('../config.json') as config_fp:
        config = json.loads(config_fp.read())
    
    try:
        subscription_key = config['subscription-key']
        resource_region = config['resource-region']
    except:
        print('Element missing from config')
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Translate text to speech.')
    parser.add_argument('--infile', help='The filename containing the text to translate', required=True)
    parser.add_argument('--outfile', help='What to save the file as, under the media/ directory', required=True)
    args = parser.parse_args()
    
    app = TextToSpeech(subscription_key, resource_region)

    with open(args.infile, encoding='utf-8') as text_fp:
        text = text_fp.read()
    app.convert(text, args.outfile)
