# import the necessary packages
from flask import Flask, render_template, Response
import numpy as np
import cv2


app = Flask(__name__)

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
"""
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))
"""

def gen_frames():  # generate frame by frame from camera
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
            frame = cv2.rectangle(frame, (xA, yA), (xB, yB),
                  (0, 255, 0), 2)

        # Write the output video
        #out.write(frame.astype('uint8'))
        # Display the resulting frame
        #cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

"""
# When everything done, release the capture
cap.release()
# and release the output
#out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
"""




@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
