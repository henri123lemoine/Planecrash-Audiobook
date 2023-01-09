import requests
import subprocess

# def login(key):
#     url = 'https://api.novelai.net/user/login'
#     headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
#     data = f'{"key": "{key}"}'

#     response = requests.post(url, headers=headers, data=data)

#     print(response.status_code)


# def get_voice(text, voice_number, filename, seed='Bob'):
#     url = 'https://api.novelai.net/ai/generate-voice'
    
#     query_params = {
#         'text': text,
#         'seed': seed,
#         'voice': voice_number,
#         'opus': 'true',
#         'version': 'v2'
#     }

#     response = requests.get(url, params=query_params)

#     if response.status_code == 200:
#         # Save the response content to an MP3 file
#         with open("response.webm", "wb") as f:
#             f.write(response.content)
#         subprocess.run([r'C:\ffmpeg\bin\ffmpeg.exe', '-i', 'response.webm', f'Audio/voice{voice_number}.wav'])
#     else:
#         print("Request failed with status code:", response.status_code)

# login()

# get_voice("This story begins in a place that would be, as seen by some other places, a high-trust society.  It happens that this place has no histories to call upon of earlier, lower-trust societies.  It is expected by this society that this historical amnesia will end up not being relevant to the vast, vast supermajority of its members.  Had they thought otherwise, they would have chosen otherwise.  They try to plan out everything important that way, and then not plan out everything else to the point where it stops being fun.  It's that kind of society, you see, the kind with prediction markets and policy goals.", 63, "intro.wav")
        
# url = 'https://api.novelai.net/ai/generate-voice'
# for i in range(1, 72, 4):
#     query_params = {
#         'text': f"Hi, this is voice number {i}.",
#         'seed': 'none',
#         'voice': f'{i}',
#         'opus': 'true',
#         'version': 'v2'
#     }

#     response = requests.get(url, params=query_params)

#     if response.status_code == 200:
#         # Save the response content to an MP3 file
#         with open("response.webm", "wb") as f:
#             f.write(response.content)
#         subprocess.run([r'C:\ffmpeg\bin\ffmpeg.exe', '-i', 'response.webm', f'Audio/voice{i}.wav'])
#     else:
#         print("Request failed with status code:", response.status_code)

# import os
# from pydub import AudioSegment

# # files = os.listdir('audio')
# # files = [f for f in files if f.endswith('.wav')]
# # files = sorted(files, key=lambda x: int(x.split('.')[0][5:]))
# # files = [f"audio/{f}" for f in files]
# files = ['Audio/Play_ht/05 - (quick) HOOOOLLLD EVERY.wav', 'Audio/Play_ht/06 - Pilar sort of wa 1.wav']

# combined = AudioSegment.empty()
# for f in files:
#     try:
#         combined += AudioSegment.from_wav(f"{f}")
#         print(f"Added file {f} successfully.")
#     except:
#         print(f"Error adding file {f}.")

# combined.export("Audio/Play_ht/02 - HOOOOLDDD EVERYTHING.wav", format="wav")




from pydub import AudioSegment
silence_duration = 400
audio1 = AudioSegment.from_file("Audio/Play_ht/09 - Keltham is none 1.wav", format="wav")
audio2 = AudioSegment.from_file("Audio/Play_ht/10 - Snack Service 1.wav", format="wav")
silence = AudioSegment.silent(duration=silence_duration)
result = audio1 + silence + audio2
result.export("Audio/Play_ht/04 - Aspexia.wav", format="wav")
