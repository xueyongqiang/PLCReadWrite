import subprocess
import time
import re

# 只靠系统语音，最稳定
def speak(text):
    # 强制单线程、等播放完才返回
    ps = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Speak(\'{text.replace("\'", "")}\');'
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def play():
    with open("script.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("===== 逐句播放开始 =====\n")

    for line in lines:
        line = line.strip()
        if not line:
            time.sleep(0.3)
            continue

        # 匹配角色
        match = re.match(r"^(.+?)[:：](.+)", line)
        if match:
            role = match.group(1).strip()
            content = match.group(2).strip()
            print(f"【{role}】{content}")
            speak(content)
        else:
            print(line)
            speak(line)

        # 关键：强制等一下，不让系统吞句子
        time.sleep(0.5)

    print("\n播放完毕")

if __name__ == "__main__":
    play()