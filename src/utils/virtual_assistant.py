import pywhatkit
import datetime

from src.utils.audio_utility import AudioUtility
from src.utils.features import Features


load_dotenv()


class VirtualAssistant:
    def __init__(self):
        self.config_json = self.read_config_json(os.getenv("config_json_path", ""))
        self.owm = pyowm.OWM(os.getenv("pyowm_key",""))
        self.audio = AudioUtility()
        self.feature = Features(self.audio, self.config_json)

    @staticmethod
    def read_config_json(path):
        """
        function to read config.json file
        :return: dictionary object
        """
        with open(path, "rb") as f:
            config_json = json.load(f)
        return config_json

    def run_alexa(self):
        """
        main function to call all the features.
        :return: True if we want to exit
        """
        command = self.audio.take_command()
        print("command :", command)
        if not command:
            pass
        elif re.search(r'\b(alexa)\b', command):
            command = command.replace('alexa', '')
            if re.search(r'\b(play)\b', command):
                song = command.split("play")[-1]
                self.audio.talk(random.choice(self.config_json["statements"]["playing"]) + song)
                pywhatkit.playonyt(song)
            elif re.search(r'\b(cases)\b', command) or re.search(r'\b(covid)\b', command):
                self.audio.talk("for which state you want covid report")
                command = self.audio.take_command()
                if not command or command not in self.config_json["states"]:
                    self.audio.talk(random.choice(self.config_json["statements"]["understand"]))
                else:
                    self.feature.get_covid_report(command)
            elif (re.search(r'\b(who)\b', command) or re.search(r'\b(what)\b', command)) \
                    and re.search(r'\b(is)\b', command):
                self.feature.search_online(command)
            elif re.search(r'\b(date)\b', command):
                self.audio.talk(random.choice(self.config_json["statements"]["date"]))
            else:
                self.audio.talk(random.choice(self.config_json["statements"]["command_not_found"]))

    
