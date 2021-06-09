###########스트리밍 되고 있는 영상 받아서 DB에 업데이트 하는코드 아직 db 안드에 알람가게 수정안함####
###안드에 알람가게 하고 싶으면 DL51_picamera_appendDB_최종.py참고
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import face_recognition
import pickle
import time
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from uuid import uuid4

import os

face_cascade_name = './haarcascades/haarcascade_frontalface_alt.xml'
face_cascade = cv2.CascadeClassifier()
# -- 1. Load the cascades
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

encoding_file = 'encodings.pickle'
# load the known faces and embeddings
data = pickle.loads(open(encoding_file, "rb").read())

# PROJECT_ID = "rasbpi-face"#내 project id
# Fetch the service account key JSON file contents
cred = credentials.Certificate('raspbpi-face-firebase-adminsdk-611sy-7b4d5c3fc2.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://raspbpi-face-default-rtdb.firebaseio.com/',
    'storageBucket': 'raspbpi-face.appspot.com'
})


def fileUpload(file):
    blob = bucket.blob(suffix)
    # blob = bucket.blob(file)
    # new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}  # access token이 필요하다.
    blob.metadata = metadata

    # upload file
    blob.upload_from_filename(filename=file, content_type='image/jpeg')
    print(blob.public_url)


# 버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
bucket = storage.bucket()  # 기본 버킷 사용

unknown_name = 'Unknown'
recognized_name = None
frame_count = 0
frame_interval = 8

frame_width = 640
frame_height = 480
frame_resolution = [frame_width, frame_height]
frame_rate = 16





# catured_image = './captureImages/'
catured_image = 'captureImages/'
# catured = open(catured_image,'wb')

# Open a sample video available in sample-videos
vcap = cv2.VideoCapture('http://58.120.85.74:8090/?action=stream')

while (vcap.isOpened()):
    ret, frame = vcap.read()
    if ret:
            start_time = time.time()
            # grab the raw NumPy array representing the image
            image = frame ######
            # store temporary catured image
            suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
            filename = './' + catured_image + suffix
            cv2.imwrite(filename, frame)    
            
            # noise cancelling
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # -- Detect faces
            faces = face_cascade.detectMultiScale(gray)

            rois = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

            encodings = face_recognition.face_encodings(rgb, rois)

            # initialize the list of names for each face detected, 이 중 제일 많이 나온 이름을 detect 할것
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = unknown_name

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number of
                    # votes (note: in the event of an unlikely tie Python will
                    # select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(rois, names):
                # draw the predicted face name on the image
                y = top - 15 if top - 15 > 15 else top + 15
                color = (0, 255, 0)
                line = 2
                if (name == unknown_name):
                    color = (0, 0, 255)
                    line = 1
                    # current = str(time.time())
                    # path = '/' + current[:10] + name + '.jpg'
                    # upload image to firebase
                    fileUpload(filename)

                if (name != recognized_name):
                    recognized_name = name
                    # Send Notice
                    print("Send Notice")
                    # current = str(time.time())
                    # path = current[:10] + name + '.jpg'
                    print(filename)
                    # cv2.imwrite(path, image)
                    pplCount=pplCount+1
                    ref = db.reference(str(pplCount))
                    ref = db.reference(name)
                    #box_ref = ref.child(name)
                    box_ref.push.set({
                        'name': name,
                        'date': time.time(),
                        'path': suffix
                    })
                    # dbx.files_upload(open(catured_image, "rb").read(), path)
                    fileUpload(filename)
                    # print(dbx.files_get_metadata(path))
                    # os.remove(filename)

                cv2.rectangle(image, (left, top), (right, bottom), color, line)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, color, line)

            end_time = time.time()
            process_time = end_time - start_time
            print("=== A frame took {:.3f} seconds".format(process_time))
            # show the output image
            cv2.imshow("Recognition", image)

            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            #rawCapture.truncate(0)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

vcap.release()
cv2.destroyAllWindows()



