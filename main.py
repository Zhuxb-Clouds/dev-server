from fastapi import FastAPI, HTTPException

import os
from typing import Dict, Tuple
from audio_process import AudioProcess


app = FastAPI()


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
