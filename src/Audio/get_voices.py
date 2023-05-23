import json
import os
import requests

import sys
sys.path.append(os.getcwd())

try:
    from config import PLAY_HT_API_KEY, PLAY_HT_USER_ID
except (ImportError, ModuleNotFoundError):
    from src.config import PLAY_HT_API_KEY, PLAY_HT_USER_ID


class Voices:
    def __init__(self, voice_data_path='data/voices.json'):
        self.voice_data_path = voice_data_path
        self.voices = None
        self.url = "https://play.ht/api/v2/voices"
        self.headers = {
            "accept": "application/json",
            "AUTHORIZATION": f"Bearer {PLAY_HT_API_KEY}",
            "X-USER-ID": PLAY_HT_USER_ID
        }
        
    def get_attribute_list(self, attribute, filtered_voices=None):
        if filtered_voices is None:
            filtered_voices = self.voices

        return [voice[attribute] for voice in filtered_voices]

    def get_voices(self, update=False):
        if update or not os.path.exists(self.voice_data_path):
            response = requests.get(self.url, headers=self.headers)
            self.voices = response.json()
            with open(self.voice_data_path, 'w') as file:
                json.dump(self.voices, file, indent=4)
        else:
            with open(self.voice_data_path, 'r') as file:
                self.voices = json.load(file)

        return self.voices

    def filter_voices(self, filter_dict):
        filtered_voices = []
        for voice in self.voices:
            match = True
            for key, value in filter_dict.items():
                if isinstance(value, list):
                    if voice[key] not in value:
                        match = False
                        break
                else:
                    if voice[key] != value:
                        match = False
                        break
            if match:
                filtered_voices.append(voice)
        return filtered_voices

    def print_voices(self, voices):
        if not voices:
            print("No voices match the filter.")
            return

        keys = list(voices[0].keys())
        max_lengths = {key: max(len(key), len(max([str(voice[key]) for voice in voices], key=len))) for key in keys}

        # Print headers
        for key in keys:
            print(f"{key:<{max_lengths[key]}}", end=' | ')
        print()
        print('-' * sum(max_lengths.values()) + '-' * len(keys) * 3)

        # Print voices
        for voice in voices:
            for key in keys:
                print(f"{str(voice[key]):<{max_lengths[key]}}", end=' | ')
            print()
            

if __name__ == '__main__':
    # Initialize with your API key and User ID
    playht = Voices()

    # Get voices and update the local file if needed
    voices = playht.get_voices(update=False)

    # Define your filter
    filter_dict = {"style": "narrative", "tempo": ["fast", "neutral"]}

    # Filter voices
    filtered_voices = playht.filter_voices(filter_dict)

    # Print filtered voices
    playht.print_voices(filtered_voices)
