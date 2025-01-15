import json
import os
import sys
import wave
from io import BytesIO

import google.generativeai as genai
import pyaudio
import requests
from dotenv_flow import dotenv_flow
from PIL import Image

# ==========================
# 変数定義
# ==========================
SPEAKER_ID = 1
prompt = """\
このレシートで買ったものと合計金額を簡潔に教えて下さい．
もし，レシートの画像でない場合は，「レシートではないですよ！」と言ってください．
"""


# ==========================
# メイン処理
# ==========================

dotenv_flow()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================
# 画像パスの取得
# ==========================
if len(sys.argv) < 2:
	print("使用方法: python main.py <画像ファイルのパス>")
	sys.exit(1)

image_path = sys.argv[1]

# ==========================
# 画像処理
# ==========================
try:
	image = Image.open(image_path)
except IOError as e:
	print("画像ファイルを開けませんでした:", e)
	sys.exit(1)

# ==========================
# テキスト生成
# ==========================
try:
	response = model.generate_content([prompt, image])
except Exception as e:
	print("文章生成に失敗しました:", e)
	sys.exit(1)

print("生成されたテキスト:", response.text)

# ==========================
# 音声合成用クエリ作成
# ==========================
query_payload = {"text": response.text, "speaker": SPEAKER_ID}
try:
	response1 = requests.post(
		"http://localhost:50021/audio_query", params=query_payload
	)
	response1.raise_for_status()
except requests.exceptions.RequestException as e:
	print("音声合成のクエリ作成に失敗しました:", e)
	sys.exit(1)

query_data = response1.json()

# ==========================
# 音声合成の実行
# ==========================
headers = {"Content-Type": "application/json"}
try:
	response2 = requests.post(
		"http://localhost:50021/synthesis",
		headers=headers,
		params={"speaker": SPEAKER_ID},
		data=json.dumps(query_data),
	)
	response2.raise_for_status()
except requests.exceptions.RequestException as e:
	print("音声合成に失敗しました:", e)
	sys.exit(1)

audio_data = BytesIO(response2.content)
with wave.open(audio_data, "rb") as wf:
	p = pyaudio.PyAudio()
	stream = p.open(
		format=p.get_format_from_width(wf.getsampwidth()),
		channels=wf.getnchannels(),
		rate=wf.getframerate(),
		output=True,
	)
	data = wf.readframes(1024)
	while data:
		stream.write(data)
		data = wf.readframes(1024)
	stream.stop_stream()
	stream.close()
	p.terminate()
