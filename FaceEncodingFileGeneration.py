import cv2
import face_recognition
import pickle

#path를 매뉴얼로 저장
dataset_paths = ['dataset/name1/', 'dataset/name2/', 'dataset/name3/']
#카테고리 이름
names = ['name1','name2', 'name3']
number_images = 10
image_type = '.jpg'
encoding_file = 'encodings.pickle'
# Either cnn  or hog. The CNN method is more accurate but slower. HOG is faster but less accurate.
model_method = 'cnn'

# 각 인물의 encoding정보를 저장하는 배열
knownEncodings = []
knownNames = []

# 데이터셋에 들어있는 사진들의 정보를 encoding
for (i, dataset_path) in enumerate(dataset_paths):
    # extract the person name from names
    name = names[i]

    for idx in range(number_images):
        file_name = dataset_path + str(idx+1) + image_type

        
        # openCV는 BGR로 되어 있는데 dlib에서는 RGB형식을 쓴다. openCV로 이미지를 읽어 들이고 RGB로 변환
        image = cv2.imread(file_name)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        
        # 사진 에서 얼굴 부분만 찾을 수 있도록 Region of Interest설정
        boxes = face_recognition.face_locations(rgb,
            model=model_method)

        # roi에서 특정 값을 추출
        encodings = face_recognition.face_encodings(rgb, boxes)

        # encodings에 여러 개의 값이 나오는데, for문을 돌면서 encoding내용을 배열에 저장
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            print(file_name, name, encoding)
            knownEncodings.append(encoding)
            knownNames.append(name)
        
# encoding값과 해당하는 이름을 pickle파일에 저장
data = {"encodings": knownEncodings, "names": knownNames}
f = open(encoding_file, "wb")
f.write(pickle.dumps(data))
f.close()
