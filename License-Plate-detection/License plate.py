# This code is for Detecting License plate from live videos.
import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

cap = cv2.VideoCapture('your_video.mp4')

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = imutils.resize(frame, width=500)

    cv2.imshow('Original Frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    smooth = cv2.bilateralFilter(gray, 11, 17, 17)

    edges = cv2.Canny(gray, 170, 200)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    image_contours = frame.copy()
    cv2.drawContours(image_contours, contours, -1, (0, 0, 255), 3)
    cv2.imshow('Edge Segmentation', image_contours)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    number_plate = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4:
            number_plate = approx
            x, y, w, h = cv2.boundingRect(contour)

            cv2.drawContours(frame, [number_plate], -1, (0, 255, 0), 3)

            cropped_image = frame[y:y + h, x:x + w]
            cv2.imshow('Number Plate', cropped_image)

    cv2.imshow('Processed Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
