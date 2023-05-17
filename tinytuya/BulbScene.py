from typing import List, Union


class SceneFrame(object):
    """
    Data layout:
        Transition Time<2 bytes>: Time to be subtracted from the base. Base = 10.5s
            Unit value = 1/2570s | 1s subtraction = 2570(0xA0A)
        Transition Type<1 byte>: Type of transition for the frame.
            0: Static | 1: Flash | 2: Breathe
        Hue<2 bytes>: Hue value represented in degrees on the color wheel. (0-360)
        Saturation<2 bytes>:  Saturation of the color represented in tenth of percents. (0-1000)
        Value<2 bytes>: Intensity of the color represented in tenth of percents. (0-1000)
        White Intensity<2 bytes>: Intensity of the white light represented in tenth of percents. (0-1000)
        White Temperature<2 bytes>: Temperature of the white light represented in tenth of percents. (0-1000)
    """
    def __init__(self,
                 frame_time: float,
                 transition: int,
                 hue: int,
                 saturation: float,
                 value: float,
                 white_intensity: float,
                 white_temp: float):
        self.TransitionSpeed = frame_time
        self.Transition = transition
        self.Hue = hue
        self.Saturation = saturation * 10
        self.Value = value * 10
        self.WhiteIntensity = white_intensity * 10
        self.WhiteTemperature = white_temp * 10

    @staticmethod
    def _validate_range(value, min_, max_):
        assert min_ <= value <= max_
        return value

    def get_data(self) -> str:
        base = 10.5 if self.Transition == 1 else 11.0
        return f"{int((base - self.TransitionSpeed) * 0xA0A):0{4}x}" \
               f"{self.Transition:0{2}x}" \
               f"{self.Hue:0{4}x}" \
               f"{self.Saturation:0{4}x}" \
               f"{self.Value:0{4}x}" \
               f"{self.WhiteIntensity:0{4}x}" \
               f"{self.WhiteTemperature:0{4}x}"


class ColorFrame(SceneFrame):
    """ Frame descriptor for colored frames.
    For more info see the SceneFrame base class"""
    def __init__(self,
                 frame_time: float,
                 transition: int,
                 hue: int,
                 saturation: float,
                 value: float):
        """
        :param frame_time: Time to spend in this frame. Range: 0.1s - 10.5s
        :param transition: How to transition into the frame. STATIC = 0x0 | FLASH = 0x1 | BREATE = 0x2
        :param hue: Hue color value in degrees. Range: 0 - 360
        :param saturation: Saturation of the color. Range: 0.0% - 100.0%
        :param value: Intensity of the color. Range: 0.1% - 100.0%
        """
        super().__init__(
            self._validate_range(frame_time, 0.1, 10.5),
            transition,
            self._validate_range(hue, 0, 360),
            self._validate_range(saturation, 0.0, 100.0),
            self._validate_range(value, 0.1, 100.0),
            0,
            0
        )


class WhiteFrame(SceneFrame):
    """ Frame descriptor for white frames.
    For more info see the SceneFrame base class"""
    def __init__(self,
                 frame_time: float,
                 transition: int,
                 white_intensity: float,
                 white_temp: float):
        """
        :param frame_time: Time to spend in this frame. Range: 0.1s - 10.5s
        :param transition: How to transition into the frame. STATIC = 0x0 | FLASH = 0x1 | BREATE = 0x2
        :param white_intensity: Intensity of the white light. Range: 0.1% - 100.0%
        :param white_temp: Temperature of the withe light. Range: 0.0% - 100.0%
        """
        super().__init__(
            self._validate_range(frame_time, 0.1, 10.5),
            transition,
            0,
            0,
            0,
            self._validate_range(white_intensity, 0.1, 100.0),
            self._validate_range(white_temp, 0.0, 100.0)
        )


class Scene(object):
    MAX_FRAME_COUNT = 8

    def __init__(self, scene_id: int, frames: List[Union[WhiteFrame, ColorFrame]] = None):
        self.ID = scene_id
        self.Frames = []
        for frame in frames:
            self.add_frame(frame)

    def add_frame(self, frame: Union[WhiteFrame, ColorFrame]):
        assert len(self.Frames) < self.MAX_FRAME_COUNT
        self.Frames.append(frame)

    def __str__(self):
        out = f"{self.ID:0{2}x}"
        for frame in list(self.Frames):
            out += frame.get_data()
        return out

    def __repr__(self):
        return self.__str__()
