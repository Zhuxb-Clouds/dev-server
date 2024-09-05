from get_script_voice import get_voice_object
from audio_process import AudioProcess
from constants import GAME_PATH
import os
from pydub import AudioSegment

# 通过get_voice_object得到所有的voiceObject，然后根据voiceObject创建AudioProcess,并应用所有的效果，最后保存到OUTPUT_PATH
INPUT_PATH = os.path.join(GAME_PATH, "voice")
OUTPUT_PATH = os.path.join(GAME_PATH, "voice_fx")


def apply_voice_fx():
    voice_object_list = get_voice_object()

    for voice_obj in voice_object_list:

        input_file_path = os.path.join(INPUT_PATH, voice_obj.voice)
        output_file_path = os.path.join(OUTPUT_PATH, voice_obj.voice)
        # 检查输入文件是否存在
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"File not found: {input_file_path}")
        if os.path.exists(output_file_path):
            print(f"File already exists: {output_file_path}")
            continue
        # 加载音频文件
        audio_process = AudioProcess(AudioSegment.from_file(input_file_path))

        # 应用所有效果
        for attr, value in voice_obj.attr.items():
            print(f"Applying {attr}={value} to {voice_obj.voice}...")
            if hasattr(audio_process, attr):
                # 如果value是形如"0.5"的字符串，那么转换成float，如果是true或者false，那么转换成bool，如果是整数，那么转换成int
                if isinstance(value, bool):
                    getattr(audio_process, attr)()
                elif value.isdigit():
                    value = int(value)
                    getattr(audio_process, attr)(value)
                elif "." in value:
                    value = float(value)
                    getattr(audio_process, attr)(value)
                
        print(f"Applying effects to {voice_obj.voice}...")
        # 保存音频文件
        audio_process.audio.export(output_file_path, format="flac")


if __name__ == "__main__":
    apply_voice_fx()
