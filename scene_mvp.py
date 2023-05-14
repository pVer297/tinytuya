from tinytuya import BulbDevice
from tinytuya.BulbScene import ColorFrame, WhiteFrame, Scene
import time


DEV_ID = ""
ADDRESS = ""
LOCAL_KEY = ""


def main():
    bulb = BulbDevice(
        dev_id=DEV_ID,
        address=ADDRESS,
        local_key=LOCAL_KEY,
        dev_type="default",
        version="3.3",
        persist=True
    )

    bulb.turn_on()
    bulb.set_mode("scene")

    red_frame = ColorFrame(1, 1, 0, 50, 20)
    lime_frame = ColorFrame(1, 1, 110, 50, 20)
    blue_frame = ColorFrame(1, 1, 240, 50, 20)
    white_frame = WhiteFrame(1, 1, 20, 20)

    scene = Scene(0, [
        red_frame,
        lime_frame,
        blue_frame,
        white_frame,
    ])

    print(bulb.send_scene(str(scene)))

    time.sleep(10)

    scene2 = Scene(1, [
        red_frame,
        blue_frame,
    ])

    print(bulb.send_scene(str(scene2)))


if __name__ == '__main__':
    main()
