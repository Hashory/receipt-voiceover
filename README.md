# Receipt Voiceover

レシート画像を読み取り、VOICEVOXで音声で読み上げるプログラムです。

## 必要な環境

- [uv](https://docs.astral.sh/uv/)
- Google Cloud Gemini API キー
- VOICEVOX

## VOICEVOXのセットアップ

1. [VOICEVOX公式サイト](https://voicevox.hiroshiba.jp/)からVOICEVOXをダウンロードしてインストールします
2. VOICEVOXインストールディレクトリ内にある`run.exe`を実行し、サーバを起動します

## セットアップ

1. リポジトリをクローンする

```bash
git clone https://github.com/hashory/receipt-voiceover.git
cd receipt-voiceover
```

2. 依存パッケージをインストール

```bash
uv sync
```

3. 環境変数の設定 `.env`ファイルを作成し、必要なAPI keyを設定してください：

```
API_KEY="your-api-key-here"
```

## 使い方

1. VOICEVOXのサーバを起動します
2. レシート画像を用意します
3. プログラムを実行します：

```bash
uv run main.py [画像ファイルのパス]
```
