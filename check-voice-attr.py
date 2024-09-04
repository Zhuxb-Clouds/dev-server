import re
import json

SCRIPTS_PATH = [
    "script.rpy",
    "script2nd.rpy",
]

FOLD_PATH = "D:/Program Files/RenPy/game/The-Roc/game/"

voice_object_list = []


class VoiceObject:
    def __init__(self, line_content, line_number, filename):
        print(line_content)
        self.voice = self.extract_filename(line_content)
        # 将任意的属性存储在字典中
        self.attr = self.extract_tag_info(line_content)
        self.line_number = line_number
        self.filename = filename

    def extract_tag_info(self, filename):
        # 使用正则表达式提取所有方括号中的内容
        pattern = r"\[(.*?)\]"
        matches = re.findall(pattern, filename)

        tag_info = {}

        for match in matches:
            # 使用逗号分隔多个属性
            attributes = match.split(",")

            for attribute in attributes:
                # 如果属性包含等号，就拆分成键值对
                if "=" in attribute:
                    key, value = attribute.split("=", 1)
                    tag_info[key.strip()] = value.strip()
                else:
                    # 如果不包含等号，作为布尔值处理
                    tag_info[attribute.strip()] = True

        return tag_info

    def extract_filename(self, filename):
        # 使用正则表达式去除方括号和其中的内容
        pattern = r"\[.*?\]"
        clean_filename = re.sub(pattern, "", filename)
        # 去除前后多余的空格
        clean_filename = clean_filename.strip()
        return clean_filename


def extract_first_quoted_content(text):
    # 匹配第一个双引号或单引号内的内容
    pattern = r'["\'](.*?)["\']'
    match = re.search(pattern, text)

    if match:
        # 返回不带引号的内容
        return match.group(1)
    return None


def get_voice_object():
    # 形如：voice "[pan=-0.2]周清-道德三皇五帝，功名夏侯商周。五霸七雄闹春秋，顷刻兴亡过手。青史几行名姓，北邙无数荒丘。前人撒种后人收，无非是龙争——虎斗！.flac"
    # 读取所有脚本文件,获取以voice为开头的行，提取文件名（周清-道德三皇...虎斗！.flac）部分，将其作为voiceObject，存入voice_object列表
    pattern = r'["\'](.*?)["\']'
    try:
        for script in SCRIPTS_PATH:

            with open(f"{FOLD_PATH}{script}", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if "voice" in line and "stop" not in line:

                        print(line)
                        voice_object_list.append(
                            VoiceObject(extract_first_quoted_content(line), i, script)
                        )
    except Exception as e:
        print(f"Error: {e}")


def check_conflict_voice():
    # 获取那些voice相同，但是属性不同的对象，输出其对象到conflict.json # Group VoiceObject instances by their 'voice' attribute
    voice_dict = {}
    for voice_obj in voice_object_list:
        key = (voice_obj.voice, voice_obj.filename)
        if key not in voice_dict:
            voice_dict[key] = []
        voice_dict[key].append(voice_obj)

    conflicts = []
    
    # Find conflicts within each group
    for (voice, filename), objs in voice_dict.items():
        if len(objs) > 1:
            # Compare attributes of all VoiceObject instances with the same 'voice' and filename
            for i in range(len(objs)):
                for j in range(i + 1, len(objs)):
                    if objs[i].attr != objs[j].attr:
                        conflicts.append({
                            'voice': voice,
                            'conflict': {
                                f"{filename}:{objs[i].line_number}": objs[i].attr,
                                f"{filename}:{objs[j].line_number}": objs[j].attr
                            }
                        })
    
    # Write conflicts to conflict.json
    with open("conflict.json", "w") as file:
        json.dump(conflicts, file, indent=2)



if __name__ == "__main__":
    get_voice_object()
    check_conflict_voice()
