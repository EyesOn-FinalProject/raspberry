from picamera import PiCamera
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import threading
import MyCamera

"""
on_connect는 subscriber가 브로커에 연결하면서 호출할 함수
rc가 0이면 정상접속이 됐다는 의미
"""

# 전역변수
uuid = ""


class Check():
    def __init__(self):
        self.data = 0

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data


class MqttCamera():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("15.164.46.54", 1883, 60)
        self.thread = None
        self.camera = MyCamera.Camera()
        self.check = Check()
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("eyeson/raspberryPi1")
        else:
            print("연결실패")

    def mywhileRun(self):
        global uuid
        while self.check.getData() == 1:
            frame = self.camera.getStreaming()
            publish.single("eyeson/" + uuid, frame, hostname="15.164.46.54")

    # 메시지가 도착됐을때 처리할 일들 - 여러가지 장비 제어하기, Mongodb에 저장
    def on_message(self, client, userdata, msg):
        global uuid
        try:
            myval = msg.payload.decode("utf-8")
            myval = myval.split("/")
            if myval[0] == "android":
                if myval[1] == "camera":
                    if myval[2] == "on":
                        uuid = myval[3]
                        print("camera on")
                        self.check.setData(1)
                        self.thread = threading.Thread(target=self.mywhileRun)
                        self.thread.start()
                    elif myval[2] == "off":
                        print("camera off")
                        self.check.setData(0)
        except:
            pass


if __name__ == "__main__":
    try:
        mymqtt = MqttCamera()

    except KeyboardInterrupt:
        print("종료")
