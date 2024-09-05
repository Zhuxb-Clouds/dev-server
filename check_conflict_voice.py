
from get_script_voice import get_voice_object


def check_conflict_voice(voice_object_list):
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
    
    check_conflict_voice(get_voice_object())
