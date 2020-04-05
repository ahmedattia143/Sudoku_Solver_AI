import cv2 as cv
import imutils
import numpy as np 
import tensorflow
from tensorflow.keras.models import load_model
model = load_model('model/model.h5')

class SudokuPreprocess:
    def __init__(self,image):
        self.image = image
        
    def sud_wrapping(self,image):

        #image = cv.resize(image,(300,300))
        print("1")
        ratio = image.shape[0]/300.0
        orig = image.copy()
        image = imutils.resize(image , height = 300)
        gray  = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray,11,17,17)
        edged = cv.Canny(gray,30,200)
        gray  = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray,11,17,17)
        edged = cv.Canny(gray,30,200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        cnts = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:10]
        screenCnt = None


        for c in cnts:
            peri = cv.arcLength(c,True)
            approx  = cv.approxPolyDP(c,0.015*peri ,True)

            if len(approx) == 4:
                screenCnt = approx 
                break

        pts = screenCnt.reshape(4,2)
        rect = np.zeros((4,2),dtype = "float32")

        s  = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts , axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        rect *= ratio 

        (tl,tr,br,bl) = rect 
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")

        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        M = cv.getPerspectiveTransform(rect, dst)
        warp = cv.warpPerspective(orig, M, (maxWidth, maxHeight))
        # reversing colors (more easy for digit recognition later)
        return warp 
    
    def pre_process_image(self,img):
        """Uses a blurring function, adaptive thresholding and dilation to expose the main features of an image."""
        #resize
        proc = cv.resize(img,(900,900))
        proc = cv.cvtColor(proc, cv.COLOR_BGR2GRAY)
        # Gaussian blur with a kernal size (height, width) of 9.

        # Note that kernal sizes must be positive and odd and the kernel must be square.

        proc = cv.GaussianBlur(proc.copy(), (9,9), 0) # IMPORTANT 

        # Adaptive threshold 
        proc = cv.adaptiveThreshold(proc, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 2)

        # Invert colours, so gridlines have non-zero pixel values.
        # Necessary to dilate the image, otherwise will look like erosion instead.
        proc = cv.bitwise_not(proc)
        return proc
    
    #return an array of images of numbers 
    def split_to_numbers(self,image):  
        shape  = image.shape[0]
        GRID = 9
        rg = np.linspace(0,shape,10)[:9].astype('int')
        h = w =  int(shape /GRID ) 
        numbers = []
        for i in rg:
            for j in rg:
                crop = image[i:i+h, j:j+w]
                numbers.append(crop)

        return numbers 
    
    #predict single number 
    def predict_number(self,image):

        image = image.reshape((100,100,1))
        tab = []
        image = image/255 
        tab.append(image)
        tab = np.array(tab)
        h = np.expand_dims(tab,axis=2)
        result = model.predict(tab)
        predicted_class = np.argmax(result[0])
        return predicted_class
    
    #predict array of numbers 
    def predict_numbers(self,number_images):
        final = []
        for i in number_images:
            nb = self.predict_number(i)
            final.append(nb)
        final = np.array(final).reshape((9,9))
        return final 
    
    #return matrix of sudoku 
    def get_sudoku_matrix(self):
        try:
            result = self.sud_wrapping(self.image)
            result = self.pre_process_image(result)
            images_numbers = self.split_to_numbers(result)
            final = self.predict_numbers(images_numbers)
            return final
        except: return("cannot get matrix from the sudoku")
    
    
