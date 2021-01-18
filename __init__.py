from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class OctoPiSkill(MycroftSkill):


    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(OctoPiSkill, self).__init__(name="OctoPiSkill")

    def initialize(self):
        self.headers = {'X-Api-Key': self.settings.get('API'),
        'Content-Type': 'application/json'} 
        self.base_url=f'{self.settings.get("url")}/api'

    @intent_handler(IntentBuilder("").require("preheat").require("printer"))
    def handle_preheat_printer_intent(self, message):
        self.preheat_bed()
        self.preheat_tool()
        self.speak_dialog("preheat.started")

    def preheat_tool(self):
        url = f'{self.base_url}/printer/tool' 
        data = {'command': 'target',
        'targets': {
            'tool0': 215
        }}
        resp = requests.post(url, data=data, headers=self.headers, , verify=False)
        print(resp.text)
        
    def preheat_bed(self):
        url = f'{self.base_url}/printer/bed' 
        data = {'command': 'target',
        'target': 60 }
        resp = requests.post(url, data=data, headers=self.headers, , verify=False)
        print(resp.text)

    def stop(self):
       return True

def create_skill():
    return OctoPiSkill()
