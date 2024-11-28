import cv2
import numpy as np
from numpy import linalg as LA


if __name__ == "__main__":
    cap = cv2.VideoCapture(-1)  # Accessing the first camera
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("It seems like a problem has occurred, try running the program again. In case the problem persists, contact support.")
            break
        
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold the image to get a binary image
        # Threshold the image to get a binary image where dark pixels remain black (0) and lighter pixels become white (255)
        ret, thresh = cv2.threshold(frame_gray, 43, 255, 0)
        
        # Find contours in the binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for c in contours:
            # Calculate moments for each contour
            M = cv2.moments(c)
            
            # Check if the moment m00 is zero to avoid division by zero
            if M["m00"] != 0:
                
                # Calculate the center of mass (centroid)
                
                if M["m10"]/10000  > 300 and M["m10"]/10000 < 600:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    mu20 = float(M["m20"] - (M["m10"]**2 /M["m00"]))
                    mu02 = float(M["m02"] - (M["m01"]**2 /M["m00"]))
                    mu11 = float(M["m11"] - (M["m10"]*M["m01"]/M["m00"]))
                    J = np.matrix([[mu20, mu11],[mu11, mu02]])
                    eigenvalues, eigenvectors = LA.eig(J)
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    if eigenvalues[0] > eigenvalues[1]:
                        angle = np.degrees(np.atan2(eigenvectors[0,0],eigenvectors[0,1]))
                    else: 
                        angle = np.degrees(np.atan2(eigenvectors[1,0],eigenvectors[1,1]))
                    print(angle)
                    print(cX)                
            else:
                # Handle the case where the contour has zero area (e.g., skip or set default coordinates)
                continue

        # Display the processed frame
        cv2.imshow('Camera', frame)
        
        # Wait for a key press and break if 'q' or 'Esc' is pressed
        key = cv2.waitKey(20)
        if key == ord('q') or key == 27:
            print("Program finished!")
            break

    # Release the camera and close any open windows
    cv2.destroyAllWindows()
    cap.release()
