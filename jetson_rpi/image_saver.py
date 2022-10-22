import requests
import json 
import time
from io import BytesIO
from PIL import Image 
import PIL
from picamera import PiCamera
import strandtest
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

waste_colors = {
   'glass': (0, 255, 0),
   'metal': (255, 0, 0),
   'organic': (100, 67, 33),
   'paper': (0, 0, 255),
   'plastic': (255, 150, 0),
   'trash': (255, 255, 255)
}

camera = PiCamera()

def record():
   print("Capturing Image")
   #camera = PiCamera()
   camera.start_preview()
   camera.capture('raspberry_photo.jpg')
   camera.stop_preview()

def crop():
   print("Cropping Image")
   im=Image.open(r"raspberry_photo.jpg")
   width, height = im.size
   print(im.size) 
   left = 0
   top = 10
   right = 4*width/5
   bottom = 3*height/4
   im1 = im.crop((left, top, right, bottom)) 
   print(im1.size)
   im1=im1.save("raspberry_photo.jpg")
   time.sleep(0.5)
   #strandtest.light(0,0,0)

def classify():
   print("Classyfing Image")
   url='http://193.226.17.131:5001/classify_prob'
   files = {'image': open('raspberry_photo.jpg','rb')}
   json_data={'filename':'raspberry_photo.jpg'}
   response=requests.post(url, files=files, data=json_data)
   result=response.json()
   print(result)
   return result
   
def dzseccon():
  print("Waiting for Jetson")
  url='http://192.168.100.52:5000/dolgozz'
  jetson_response=requests.get(url)
  print(jetson_response.json())
  return jetson_response

def compare():
   inductive=GPIO.input(11)
   rpi_result=classify()
   jetson_result=dzseccon().json()
   print("Comparing results")
   avarage = dict()
   for key in rpi_result.keys():
      if key == 'metal':
         if inductive == GPIO.LOW:
            print("metal")
            avarage[key] = (float(rpi_result[key]) + float(jetson_result[key]))*2.0 / 2
         else:
            avarage[key] = (float(rpi_result[key]) + float(jetson_result[key])) / 2
      else:
         if GPIO.input(11) == GPIO.LOW:
            avarage[key] = (float(rpi_result[key]) + float(jetson_result[key]))*0.5 / 2
         else:
            avarage[key] = (float(rpi_result[key]) + float(jetson_result[key])) / 2

   print(avarage)
   max_key = 'glass'
   max_value = 0.0
   for key in  avarage.keys():
      if float(avarage[key]) > max_value:
         max_key = key
         max_value = avarage[key]

   r, g, b = waste_colors[max_key]
   strandtest.light(r, g, b)
   time.sleep(5)
   strandtest.light(0,0,0)

def exec():
   record()
   #crop()
   #classify()
   #dzseccon()
   compare()
