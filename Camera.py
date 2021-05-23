from picamera import PiCamera
from time import sleep
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

"""
on_connect는 subscriber가 브로커에 연결하면서 호출할 함수
rc가 0이면 정상접속이 됐다는 의미
"""


def on_connect(client, userdata, flags, rc):
    print("connect.." + str(rc))
    if rc == 0:
        client.subscribe("eyeson/#")
    else:
        print("연결실패")


# 메시지가 도착됐을때 처리할 일들 - 여러가지 장비 제어하기, Mongodb에 저장
def on_message(client, userdata, msg):
    myval = msg.payload.decode("utf-8")
    myval = myval.split("/")
    if myval[0] == "camera":
        if myval[1] == "on":
            uuid = myval[2] # myval[2]는 uuid
            camera = PiCamera() # PiCamera객체 생성
            camera.rotation = 180
            sleep(2) # 최소 2초 정도는 이미지 캡처하기 전에 시간을 delay
            # 카메라 센서가 빛을 감지하기 위한 시간
            camera.capture('/home/pi/eyeson/{}.jpg' %uuid)
            f = open('/home/pi/eyeson/{}.jpg' % uuid,'rb') #파일 열기(rb는 바이너리파일 읽기)
            imageString = f.read() #읽은 내용을 imageString변수에 저장
            data = bytes(imageString) #바이트로 변환
            print(data)
            publish.single("eyeson/camera",data,hostname = "15.164.46.54") #데이터 전송
            f.close() #파일 닫기
            


mqttClient = mqtt.Client()  # 클라이언트 객체 생성
# 브로커에 연결이되면 내가 정의해놓은 on_connect함수가 실행되도록 등록
mqttClient.on_connect = on_connect

# 브로커에서 메시지가 전달되면 내가 등록해 놓은 on_message함수가 실행
mqttClient.on_message = on_message

# 브로커에 연결하기
mqttClient.connect("15.164.46.54", 1883, 60)

# 토픽이 전달될때까지 수신대기
mqttClient.loop_forever()


