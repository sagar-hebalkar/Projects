from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import CustomVideoObjectDetection
from django.conf import settings
import os, shutil

model_path = "trained_model/models/detection_model-ex-038--loss-0017.520.h5"
json_path = "trained_model/json/detection_config.json"
detected_obj_from_video = set()
minimum_percentage_probability = 90

def detectAerialObjFromImage(input_path,file_name):
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()

    output_path = os.path.join(settings.MEDIA_ROOT,"output_img",file_name)
    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path,minimum_percentage_probability=minimum_percentage_probability)
    if not detection:
        shutil.move(output_path,os.path.join(settings.MEDIA_ROOT,"unidentified_img",file_name))
    return detection

def forFrame(frame_number, output_array, output_count):
    for obj_name in output_count.keys():
        detected_obj_from_video.add(obj_name)
    print("FOR FRAME " , frame_number)
    print("Output for each object : ", output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")

def detectAerialObjFromVideo(input_path,file_name):
    detected_obj_from_video.clear()
    detector = CustomVideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()

    output_path = os.path.join(settings.MEDIA_ROOT,"output_video",file_name)
    detector.detectObjectsFromVideo(input_file_path=input_path,output_file_path=output_path,log_progress=True,
                frames_per_second=10,minimum_percentage_probability=minimum_percentage_probability, per_frame_function=forFrame)
            
    return detected_obj_from_video