import cv2
import numpy as np

import cvlib as cv
from cvlib.object_detection import draw_bbox





def facee_detect(img):
    faceCascade = cv2.CascadeClassifier(
        './model/mobilenet/model.ckpt-906808.data-00000-of-00001')
    # Detect faces with Haarcascade
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return img


def face_detect(img):
    faceCascade = cv2.CascadeClassifier(
        './cascades/haarcascade_frontalface_default.xml')
    # Detect faces with Haarcascade
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return img


def object_detect_cvlib(img):
    # Perform the object detection
    bbox, label, conf = cv.detect_common_objects(
        img, confidence=0.25, model='yolov3-tiny', enable_gpu=False)
    return draw_bbox(img, bbox, label, conf)


def gender_recog_cvlib(img):
    padding = 20
    # apply face detection
    faces, confidences = cv.detect_face(img)
    # loop through detected faces
    for idx, f in enumerate(faces):
        (startX, startY) = max(0, f[0]-padding), max(0, f[1]-padding)
        (endX, endY) = min(
            img.shape[1]-1, f[2]+padding), min(img.shape[0]-1, f[3]+padding)

        # draw rectangle over face
        cv2.rectangle(img, (startX, startY),
                      (endX, endY), (0, 255, 0), 2)

        face_crop = np.copy(img[startY:endY, startX:endX])

        # apply face detection
        (label, confidence) = cv.detect_gender(face_crop)

        idx = np.argmax(confidence)
        label = label[idx]

        label = "{}: {:.2f}%".format(label, confidence[idx] * 100)

        Y = startY - 10 if startY - 10 > 10 else startY + 10

        # write detected gender and confidence percentage on top of face rectangle
        img = cv2.putText(img, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                          (0, 255, 0), 2)
    return img

def face_detect_cvlib(img):
    # apply face detection
    faces, confidences = cv.detect_face(img)
    # loop through detected faces
    for idx, f in enumerate(faces):
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]
        # draw rectangle over face
        cv2.rectangle(img, (startX, startY),
                      (endX, endY), (0, 255, 0), 2)
        text = "{:.2f}%".format(confidences[idx] * 100)
        Y = startY - 10 if startY - 10 > 10 else startY + 10
        # write confidence percentage on top of face rectangle
        img = cv2.putText(img, text, (startX, Y), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.7,
                          (0, 255, 0), 2)
    return img


