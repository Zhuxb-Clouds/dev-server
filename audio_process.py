
import pydub.scipy_effects


class AudioProcess:
    def __init__(self, audio):
        self.audio = audio

    def pan(self, pan):
        self.audio = self.audio.pan(pan)
        return self

    def gain(self, gain):
        self.audio = self.audio.apply_gain(gain)
        return self

    def fadeIn(self, fadeIn):
        try:
            # 确保 fadeIn 是一个数字类型
            fadeIn = float(fadeIn)
            # 将秒数转换成毫秒
            fadeIn_ms = int(fadeIn * 1000)
            # 应用 fade in 效果
            self.audio = self.audio.fade_in(fadeIn_ms)
        except ValueError:
            print("Invalid fadeIn value: must be a number.")
        except TypeError:
            print("Invalid fadeIn type: must be a float or int.")
        return self

    def fadeOut(self, fadeOut):
        try:
            # 确保 fadeOut 是一个数字类型
            fadeOut = float(fadeOut)
            # 将秒数转换成毫秒
            fadeOut_ms = int(fadeOut * 1000)
            # 应用 fade out 效果
            self.audio = self.audio.fade_out(fadeOut_ms)
        except ValueError:
            print("Invalid fadeOut value: must be a number.")
        except TypeError:
            print("Invalid fadeOut type: must be a float or int.")
        return self

    def highPass(self, highPass):
        try:
            # 确保 highPass 是一个数字类型
            highPass = float(highPass)
            # 应用高通滤波器
            highPass = highPass * 1000
            self.audio = self.audio.high_pass_filter(highPass)
        except ValueError:
            print("Invalid highPass value: must be a number.")
        except TypeError:
            print("Invalid highPass type: must be a float or int.")
        return self

    def lowPass(self, lowPass):
        try:
            # 确保 lowPass 是一个数字类型
            lowPass = float(lowPass)
            # 应用低通滤波器
            # 乘以1000是因为pydub的低通滤波器的频率单位是Hz
            lowPass = lowPass * 1000
            self.audio = self.audio.low_pass_filter(lowPass, order=4)
        except ValueError:
            print("Invalid lowPass value: must be a number.")
        except TypeError:
            print("Invalid lowPass type: must be a float or int.")
        return self

    def telephone(self):

        # 添加带通滤波器,模拟电话频带
        self.audio = self.audio.low_pass_filter(3000).high_pass_filter(300)

        return self
