# Installing ImageAI

ImageAI requires that you have Python 3.7.6 installed as well as some other Python libraries and frameworks. Before you install ImageAI, you must install the following dependencies.

`pip install -r requirements.txt`
<br><br>

# Downloading Model
**Download trained model from below link and move .h5 model file into directory => \aerialdetection\trained_model\models**
<br>

[Trained Model Download Link](https://static.ddl-secure.workers.dev/0:/detection_model-ex-038--loss-0017.520.h5)
<br><br>

# Mandatory Changes
**Before run this project, you have to do some necessary changes,**

*Kindly find out python installed directory and Open File => **/Python37\Lib\site-packages\imageai\Detection\Custom\__init__.py** and replace modified code with original code,*


<br>

> Original Code (Line No. : 1029)
```python
output_video = cv2.VideoWriter(output_video_filepath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                frames_per_second,
                                (frame_width, frame_height))
```

<br>

> Modified Code (Line No. : 1029)
```python
output_video = cv2.VideoWriter(output_video_filepath, cv2.VideoWriter_fourcc(*"H264"),
                                frames_per_second,
                                (frame_width, frame_height))
```

<br>

# Run This Project
`python manage.py migrate` <br>
`python manage.py runserver`