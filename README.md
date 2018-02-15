# Facial Validation

### About

This application detects whether listings of paired pictures are of the same person. It is most often used to help ensure the same person is being interviewed across waves or to detect when someone enrolls more than once in a program. Though this tool can be helpful, ensuring identity is ultimately still your responsibility.

You can help make this tool better, or have it customized to your needs, by working with GRDS on your upcoming project that involves participant photos.

### How to Use

1. Take photographs of participants in line with [the guidelines](https://github.com/PovertyAction/Facial-Validation/blob/master/Photography%20Guidelines%20for%20Facial%20Validation.pdf).
- The best way to ensure success is to train enumerators, pilot field photography and data collection, and work with GRDS to ensure the pictures collected during pilot are able to be successfully analyzed by the tool. GRDS can also continue to monitor photo quality throughout data collection. 

2. Place all images in a single folder on your machine and prepare [the input template](https://github.com/PovertyAction/Facial-Validation/blob/master/input_template.xlsx). You'll provide the path to the directory containing the images, and paired image filenames to compare.

3. Download the application from the latest [release](https://github.com/PovertyAction/Facial-Validation/releases). Run the application and follow the instructions to upload the input template.

4. Examine the output file, results.csv in the folder containing the images. A '1' on the threshold test denotes that the person in the image pair is the same, while a '0' indicates that they appear not to be.

### Help and Support
Please check the issues section on GitHub for previously solved issues. If no solution is available there feel free to open an issue; the author will attempt to respond in a reasonably timely fashion. If your request is urgent you may contact researchsupport@poverty-action.org

### Contributing
We welcome contributions in any form! To contribute please fork the project make your changes and submit a pull request. We will do our best to work through any issues with you and get your code merged into the main branch.

### Citing
If you have used this application in a study or publication, please use the following:

Jacobson, J. Innovations for Poverty Action: Facial Validation. 2017. https://github.com/PovertyAction/PII_detection

### Credit
King, D. High Quality Face Recognition with Deep Metric Learning. [online] Blog.dlib.net. Available at: http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html [Accessed 8 Feb. 2018].

### Licensing
This project is [MIT Licensed](https://github.com/PovertyAction/Facial-Validation/blob/master/LICENSE).
