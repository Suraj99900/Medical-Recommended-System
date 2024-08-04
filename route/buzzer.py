from flask import Blueprint, Response, render_template
import cv2
from imutils import face_utils
import dlib
from scipy.spatial import distance
import pygame

# Initialize camera and other necessary variables
camera = cv2.VideoCapture(0)
thresh = 0.25
frame_check = 20
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./model/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
flag = 0

# Initialize pygame
pygame.mixer.init()
# Load custom sound file
custom_sound_path = "./assets/alert-102266.mp3"
pygame.mixer.music.load(custom_sound_path)

# Create a Blueprint instance for user authentication
user_bp = Blueprint('user_bp', __name__, url_prefix='/')

# Route for user login
@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/home')
def homeScreen():
    return render_template('homeScreen.html')

@user_bp.route('/camera')
def camera_show():
    return render_template('camera.html')


def analyze_frame(frame, gray):
    global flag  # Declare flag as global
    global thresh, frame_check, detector, predictor, lStart, lEnd, rStart, rEnd

    subjects = detector(gray, 0)
    for subject in subjects:
        shape = predictor(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
        if ear < thresh:
            flag += 1
            print(flag)
            if flag >= frame_check:
                pygame.mixer.music.play()
                cv2.putText(frame, "***************************ALERT!****************************", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "***************************ALERT!****************************", (10,470),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            flag = 0

    return frame


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def gen_frames():  
    global flag  # Use the global flag variable

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = analyze_frame(frame, gray)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@user_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@user_bp.route('facts')
def factsScreen():
     return render_template('factsScreen.html')

@user_bp.route('about')
def aboutScreen():
     return render_template('aboutScreen.html')