import dlib
import sys
from tqdm import tqdm #Optional, for tracking progress of for loop
import os
from skimage import io
from sklearn.metrics.pairwise import euclidean_distances

# Set-up of parameters
## Facial detection
detector = dlib.get_frontal_face_detector()

## Landmark extraction
if hasattr(sys, "_MEIPASS"):
    predictor_path = os.path.join(sys._MEIPASS, 'shape_predictor_68_face_landmarks.dat')
else:
    predictor_path = 'shape_predictor_68_face_landmarks.dat'

sp = dlib.shape_predictor(predictor_path)

## Facial recognition
if hasattr(sys, "_MEIPASS"):
    face_rec_model_path = os.path.join(sys._MEIPASS, 'dlib_face_recognition_resnet_model_v1.dat')
else:
    face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'

facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def process_images(file_pairings):
    '''
    file_pairings is a df in which the first 2 columns have the urls of files to compare
    '''
    # Precision parameter (lower number = faster runtime, less accuracy; speed of 1 -> 99.13% accuracy, 100 -> 99.38%)
    speed = 1

    ## Track and store information on each image as it is processed, as well as score; set Match Score default as missing
    file_pairings['Img1 Processed?'] = ''
    file_pairings['Img2 Processed?'] = ''
    file_pairings['Img1 Vector'] = ''
    file_pairings['Img2 Vector'] = ''
    file_pairings['Match Score'] = float(-222)

    for row_index in range(file_pairings.shape[0]):
        for col_index in range(2):
            
            # Check for missing image; skip if missing
            image_path = file_pairings.iloc[row_index, col_index]
            
            # Read image and detect faces
            try:
                read_in_image = io.imread(image_path)

            except IOError:
                if col_index == 0:
                    #file_pairings['Img1 Processed?'][row_index] = 0
                    file_pairings['Img1 Processed?'][row_index] = 'File not found.'
                elif col_index == 1:
                    #file_pairings['Img2 Processed?'][row_index] = 0
                    file_pairings['Img2 Processed?'][row_index] = 'File not found.'
                continue
            
            faces = detector(read_in_image, 1)
            
            # If there is not exactly 1 face, skip
            if len(faces) != 1:
                if col_index == 0:
                    #file_pairings['Img1 Processed?'][row_index] = 0
                    file_pairings['Img1 Processed?'][row_index] = str(len(faces)) + ' faces found.'
                elif col_index == 1:
                    #file_pairings['Img2 Processed?'][row_index] = 0
                    file_pairings['Img2 Processed?'][row_index] = str(len(faces)) + ' faces found.'
                continue
      
            # Process the face and make vector
            shape = sp(read_in_image, faces[0])
            
            face_descriptor = facerec.compute_face_descriptor(read_in_image, shape, speed)        
            
            # Log successful processing and 128D vector
            if col_index == 0:
                file_pairings['Img1 Processed?'][row_index] = 1
                file_pairings['Img1 Vector'][row_index] = face_descriptor
            elif col_index == 1:
                file_pairings['Img2 Processed?'][row_index] = 1
                file_pairings['Img2 Vector'][row_index] = face_descriptor

            # If pair of images successfully processed, compute Euclidean distance
            if file_pairings['Img1 Processed?'][row_index] == 1 and file_pairings['Img2 Processed?'][row_index] == 1:
                file_pairings['Match Score'][row_index] = euclidean_distances([file_pairings['Img1 Vector'][row_index]], [file_pairings['Img2 Vector'][row_index]])[0][0]

    status_message = 'Images processed, results being calculated...'
    return status_message, file_pairings

def compare_images(file_pairings):
    threshold = 0.6 # Recommended accuracy from developers of model.
    percentage = 0
    # Flagging calculated scores that exceed Euclidean distance threshold
    if threshold != 0: # pass threshold = 0 to skip test
        file_pairings['Same Person: Threshold Test'] = ''
        
        for row_index in range(len(file_pairings)):
            # Check for valid Match Score and Score less than set threshold
            if file_pairings['Match Score'][row_index] != -222 and file_pairings['Match Score'][row_index] < threshold:
                file_pairings['Same Person: Threshold Test'][row_index] = 1.0
            elif file_pairings['Match Score'][row_index] != -222 and file_pairings['Match Score'][row_index] > threshold:
                file_pairings['Same Person: Threshold Test'][row_index] = 0.0
            elif file_pairings['Match Score'][row_index] == -222:
                file_pairings['Same Person: Threshold Test'][row_index] = -222
    
    # Flagging a set percentage of calculated scores, by greatest distance
    if percentage != 0: # pass percentage = 0 to skip test
        file_pairings['Same Person: Percentage Test'] = -222
        
        # Consider only valid values
        num_valid_values = len(file_pairings[file_pairings['Match Score']!=-222])
        minimum_valid_score = min(file_pairings[file_pairings['Match Score']!=-222]['Match Score'])
        
        # Sort by match score, figure out valid index range
        file_pairings = file_pairings.sort_values('Match Score')
        file_pairings.index = range(len(file_pairings))
        lowest_valid_value_index = list(file_pairings['Match Score']).index(minimum_valid_score)
        
        # Identify index cut-off based on specified percentage
        percent_index_highest_valid = int(num_valid_values * (1-percentage)) + lowest_valid_value_index #int rounds down, but the 0 index also means that 1 extra is being counted anyway
        
        # Assign
        file_pairings['Same Person: Percentage Test'][:lowest_valid_value_index] = -222
        file_pairings['Same Person: Percentage Test'][lowest_valid_value_index:percent_index_highest_valid] = 1
        file_pairings['Same Person: Percentage Test'][percent_index_highest_valid:] = 0

    status_message = "Application finished. Results of analysis have been output to: results.csv"
    return status_message, file_pairings