from fastapi import FastAPI, HTTPException
from pydub import AudioSegment
import pydub.scipy_effects
import os
from typing import Dict, Tuple

app = FastAPI()

# 定义常量
INPUT_PATH = "D:/Program Files/RenPy/game/The-Roc/game/voice"
OUTPUT_PATH = "D:/Program Files/RenPy/game/The-Roc/game/voice_fx"

# 初始化缓存字典
cache: Dict[str, Tuple[float, float]] = {}


class AudioProcess:
    def __init__(self, audio):
        self.audio = audio

    def pan(self, pan):
        self.audio = self.audio.pan(pan)
        return self

    def apply_gain(self, gain):
        self.audio = self.audio.apply_gain(gain)
        return self

    def fade_in(self, fadeIn):
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

    def fade_out(self, fadeOut):
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

    def high_pass_filter(self, highPass):
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

    def low_pass_filter(self, lowPass):
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

    def apply_telephone_effect(self):

        # 添加带通滤波器,模拟电话频带
        self.audio = self.audio.low_pass_filter(3000).high_pass_filter(300)

        return self


@app.get("/getVoice")
async def get_voice(
    fileName: str,
    pan: float = 0.0,
    gain: float = 0.0,
    fadeIn=0,
    fadeOut=0,
    highPass=0,
    lowPass=0,
    telephone=False,
):
    # 输出所有非零参数
    print(f"fileName: {fileName}")

    input_file_path = os.path.join(INPUT_PATH, fileName)
    output_file_name = f"{fileName}"
    output_file_path = os.path.join(OUTPUT_PATH, output_file_name)

    # 检查输入文件是否存在
    if not os.path.exists(input_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 检查缓存
    # if fileName in cache and cache[fileName] == (pan, gain, fadeIn, fadeOut, highPass, lowPass):
    #     return {
    #         "message": "File processed successfully (from cache)",
    #         "output_file": output_file_name,
    #     }

    try:

        # 加载音频文件
        audio_process = AudioProcess(AudioSegment.from_file(input_file_path))

        # 应用pan和gain
        if pan != 0.0:
            print(f"pan: {pan}")
            audio_process.pan(pan)
        if gain != 0:
            print(f"gain: {gain}")
            audio_process.apply_gain(gain)
        if fadeIn != 0:
            print(f"fadeIn: {fadeIn}")
            audio_process.fade_in(fadeIn)
        if fadeOut != 0:
            print(f"fadeOut: {fadeOut}")
            audio_process.fade_out(fadeOut)
        if highPass:
            print(f"highPass: {highPass}")
            audio_process.high_pass_filter(highPass)
        if lowPass:
            print(f"lowPass: {lowPass}")
            audio_process.low_pass_filter(lowPass)
        if telephone:
            print(f"telephone")
            audio_process.apply_telephone_effect()
        # 保存修改后的音频文件
        audio_process.audio.export(output_file_path, format="flac")

        # 更新缓存
        cache[fileName] = (pan, gain)

        return {
            "message": "File processed successfully",
            "output_file": output_file_name,
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8808)
