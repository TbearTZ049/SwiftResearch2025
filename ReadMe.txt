# Burst Chaser v2

This will be a guide on how use and recreate all data for burst chaser
that was previously used by Carter Murawski. It will explain how to download the
initial CSV and what code to run to get each resulting data point. For a more detailed
look into the math and machine learning, please refer to the overleaf document within
this folder which contains Carter's Research paper. 

Downloading Classifications CSV from Zooniverse 

    1. Go to Zooniverse Burst Chaser and log into your account
    2. Navigate to the Lab section 
    3. Find Data Exports
    4. Request a new classification export 
        a. This may take a while due to Zooniverse system, but you will get 
            an email notifying you when things are ready. 
    5. Download your Data Export 

    This export will consist of classifications from all of the citizen science surveys

Reading the Classifications CSV

    1. Have Classifications CSV in your computer or folder. 
    2. Navigate to the ReadDataExport file
    3. Ajust the CSV it is running
    4. When Ran All CSVS will be updated 

Label Bursts with Classifications

    1. Locate Prop_Freq_Verify
    2. When ran it will use your previosly created Pulse_Shapes CSV
        and Label bursts based of proportional data and frequency statistics.
    3. Output Can be found in classified bursts.

Create Image Processing and Machine Learning Labels

    1.Processing Images and Create ML by running Proccess_Images.py file
    2.ImageRecognition will create a machine learning algorithm to classify
    3.Generate_ml_to_csv creates a csv that labels bursts based off machine learning


Pulse Locations and Painting Boxes 
    1. KmeanLocation.py because all of your location results are in a csv you will use this file
        to eliminate some of the boxes. 
    2. Then run PaintBoxes.py to create images with the narrowd down boxes
        results will be in the. 


