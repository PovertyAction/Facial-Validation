# Facial Validation

### About

This application detects whether listings of paired pictures are of the same person. It is most often used to help ensure the same person is being interviewed across waves or to detect when someone enrolls more than once in a program. Though this tool can be helpful, ensuring identity is ultimately still your responsibility.

This tool is current listed as an alpha release because it is untested on IPA field pictures. You can help make this tool better, or have it customized to your needs, by working with GRDS on your upcoming project that involves participant photos.

### How to Use

There are two alternatives to use this application, with and without GUI (user interface).

#### Using app with GUI

1. Take photographs of participants in line with [the guidelines](https://github.com/PovertyAction/Facial-Validation/blob/master/Photography%20Guidelines%20for%20Facial%20Validation.pdf).
- The best way to ensure success is to train enumerators, pilot field photography and data collection, and work with GRDS to ensure the pictures collected during pilot are able to be successfully analyzed by the tool. GRDS can also continue to monitor photo quality throughout data collection.

2. Place all images in a single folder on your machine and prepare [the input template](https://github.com/PovertyAction/Facial-Validation/blob/master/input_template.xlsx). You'll provide the path to the directory containing the images, and paired image filenames to compare.

3. Download the application from the latest [release](https://github.com/PovertyAction/Facial-Validation/releases). Run the application and follow the instructions to upload the input template.

4. Examine the output file, results.csv in the folder containing the images. A '1' on the threshold test denotes that the person in the image pair is the same, while a '0' indicates that they appear not to be.

#### Using app without GUI

In case you would like to run the app without user interaction, please follow the following steps:

1. Place baseline and follow-up survey pictures in two different folders. Baseline pictures are expected to be named after their caseid, follow-up survey pictures are not. You should also have handy your survey database, which will enable the program to match follow-up survey pictures with their casesids.

2. Download the gui_less_app.exe file from the dist folder in this repository.

3. From command line, run `./gui_less_app.exe path_to_folder_with_baseline_pictures path_to_folder_with_follow_up_survey_pictures survey.dta`

4. Examine the output file, results.csv in the folder where you run the `.exe.`

#### Launching app for testing

Run `python desktop_app_frontend.py`. Install dependencies python dependencies with `pip install -r requirements.txt`.

### To create .exe from source file for GUI app

`pyinstaller --onefile --windowed --icon=app.ico --add-data="app.ico;." --add-data="ipa logo.jpg;." --add-data="shape_predictor_68_face_landmarks.dat;." --add-data="dlib_face_recognition_resnet_model_v1.dat;." desktop_app_frontend.py`

`pyinstaller --onefile --add-data="shape_predictor_68_face_landmarks.dat;." --add-data="dlib_face_recognition_resnet_model_v1.dat;." gui_less_app.py`

To create windows application installer, follow [this](https://www.youtube.com/watch?v=RrpvNvklmFA https://www.youtube.com/watch?v=DTQ-atboQiI&t=135s) tutorial:  (same approach as used in the [PII Detector](https://github.com/PovertyAction/PII_detection#to-create-windows-application-installer)

### Citing
If you have used this application in a study or publication, please use the following:

GRDS Team. Innovations for Poverty Action: Facial Validation. 2017. https://github.com/PovertyAction/PII_detection

### Credit
King, D. High Quality Face Recognition with Deep Metric Learning. [online] Blog.dlib.net. Available at: http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html [Accessed 8 Feb. 2018].

### Licensing
This project is [MIT Licensed](https://github.com/PovertyAction/Facial-Validation/blob/master/LICENSE).
