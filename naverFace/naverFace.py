# -*- coding: UTF-8-*-
import os
import sys
import win32com.client
import urllib.request
import requests
import json
import cv2
# from pprint import pprint

fileName = "5"

image = cv2.imread(fileName + ".jpg")
cv2.imshow("Face Recognition", image)
cv2.waitKey(0)
# cv2.destroyAllWindows()


# openCV webcam
# ========== From ===========
# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# while(cap.isOpened()):
#    ret, frame = cap.read()
#    # out.write(frame)
#    cv2.imshow('frame',frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#       break
# cap.release()
# cv2.destroyAllWindows()
# ========== End ==========



# Naver Face Recognition
# ========== From ===========
client_id = "client_id"
client_secret = "client_secret"
# url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
url = "https://openapi.naver.com/v1/vision/celebrity" # 유명인 얼굴인식
files = {'image': open(fileName + '.jpg', 'rb')}
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
response = requests.post(url, files=files, headers=headers)
rescode = response.status_code
if(rescode == 200):
    datajson = response.json()

    # encoding json & save json file
    dataString = json.dumps(datajson, indent=4)
    print(datajson)
    with open("response.json", 'w') as f:
        json.dump(datajson, f)
else:
    print("Error Code: " + rescode)
# ========== End ==========

# Json Enceding & Decoding
# ========== From ===========
with open('response.json') as data_file:
    data = json.load(data_file)
# data = json.loads(dataString)
# pprint(data)
same = data["faces"][0]["celebrity"]["value"]
# age = data["faces"][0]["age"]["value"]
# age = age.split('~')[1]
# emotion = data["faces"][0]["emotion"]["value"]
# gender = data["faces"][0]["gender"]["value"]
#
# if(gender == "male"):
#     genderkr = "남자네?"
# else:
#     genderkr = "여자잖아?"
#
# if(emotion == "neutral"):
#     emotionkr = "넌 감정을 잘 드러내지 않는구나?"
# elif(emotion == "smile"):
#     emotionkr = "어? 쪼개?"
# elif (emotion == "angry"):
#     emotionkr = "가. 가란말이야! 너때문에 되는일이 하나도없어!!"
# elif(emotion == "disgust"):
#     emotionkr = "토나와?"
# elif(emotion == "laugh"):
#     emotionkr = "와 존나 크게 웃네. 세상 많이 좋아졌다."
# elif(emotion == "suprise"):
#     emotionkr = "개깜놀."
# elif(emotion == "talking"):
#     emotionkr = "누가 이야기 하래?"
# elif (emotion == "sad"):
#     emotionkr = "개슬픔"
# else:
#     emotionkr = "몰라."

# ========== SPVoice TTS ==========
tts = win32com.client.Dispatch('Sapi.SpVoice')
tts.Voice = tts.GetVoices().Item(0)
# tts.Speak(age + "세. " + genderkr + ". " + emotionkr + ".")
tts.Speak("이쁘네! " + same + " 닮았네?")
# ========== End  ==========

# ========== Naver TTS ==========
tts_client_id = "tts_client_id"
tts_client_secret = "tts_client_secret"

encText = urllib.parse.quote("이쁘네! " + same + " 닮았네?")
# encText = urllib.parse.quote(age + "세. " + genderkr + ". " + emotionkr + ".")
data = "speaker=mijin&speed=0&text=" + encText;
url = "https://openapi.naver.com/v1/voice/tts.bin"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", tts_client_id)
request.add_header("X-Naver-Client-Secret", tts_client_secret)
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()
if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.read()
    with open('poem.mp3', 'wb') as f:
        f.write(response_body)
    os.system("poem.mp3")
else:
    print("Error Code:" + rescode)
