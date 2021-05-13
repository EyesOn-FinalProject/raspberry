from picamera import PiCamera
from time import sleep
import paho.mqtt.publish as publish

camera = PiCamera() # PiCamera객체 생성
camera.rotation = 180
camera.start_preview() # 미리보기 화면을 시작
sleep(10) # 최소 2초 정도는 이미지 캡처하기 전에 시간을 delay
# 카메라 센서가 빛을 감지하기 위한 시간
camera.capture('/home/pi/eyeson/image.jpg')
camera.stop_preview() # 미리보기 화면 정지


f = open('/home/pi/eyeson/image.jpg','rb') #파일 열기(rb는 바이너리파일 읽기)
imageString = f.read() #읽은 내용을 imageString변수에 저장
data = bytes(imageString) #바이트로 변환
print(data)
publish.single("eyeson/camera",data,hostname = "15.164.46.54") #데이터 전송
f.close() #파일 닫기
