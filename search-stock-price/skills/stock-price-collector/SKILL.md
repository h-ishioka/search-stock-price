---
name: stock-price-collector
description: >
  yfinance (Yahoo Finance) を使って株価データを収集・分析するスキル。
  以下のようなリクエストで使用する:
  - 現在株価の取得 (「AAPLの現在株価を教えて」「トヨタの株価は？」)
  - 過去の株価履歴の取得 (「Appleの過去1年の株価推移を見せて」)
  - 複数銘柄の一括取得・比較 (「AAPL, MSFT, GOOGの株価を一覧で」)
  - 財務指標の取得 (「NVIDIAのPERや配当利回りを調べて」「財務情報を確認したい」)
  - 株価分析・レポート作成 (「テック株をまとめて比較して」)
---

# Stock Price Collector

## 概要

yfinanceライブラリを通じてYahoo Financeから株価データを取得する。
`scripts/fetch_stock.py` を実行するか、yfinanceを直接コードで使って対応する。

## 依存関係の確認

```bash
pip install yfinance
python -c "import yfinance; print('OK')"
```

## タスク別の対応方法

### 現在株価の取得

```bash
python skills/stock-price-collector/scripts/fetch_stock.py \
  --mode current --symbols AAPL MSFT --output table
```

または直接コード:

```python
import yfinance as yf
hist = yf.Ticker("AAPL").history(period="2d")
price = hist.iloc[-1]["Close"]
```

### 過去の履歴データ

```bash
python skills/stock-price-collector/scripts/fetch_stock.py \
  --mode history --symbols AAPL --period 1mo --interval 1d
```

period: `1d` `5d` `1mo` `3mo` `6mo` `1y` `2y` `5y` `max`
interval: `1m` `1h` `1d` `1wk` `1mo`

### 複数銘柄の一括取得

```bash
python skills/stock-price-collector/scripts/fetch_stock.py \
  --mode current --symbols AAPL MSFT GOOG AMZN NVDA --output table
```

複数銘柄の履歴を同時取得する場合は `yf.download()` が効率的:

```python
import yfinance as yf
df = yf.download(["AAPL", "MSFT", "GOOG"], period="1mo")
closes = df["Close"]  # 各銘柄の終値
```

### 財務指標の取得

```bash
python skills/stock-price-collector/scripts/fetch_stock.py \
  --mode info --symbols AAPL MSFT
```

主な財務指標: PER (`trailingPE`), PBR (`priceToBook`), 配当利回り (`dividendYield`),
ROE (`returnOnEquity`), 目標株価 (`targetMeanPrice`)

## ティッカーシンボルの形式

| 市場 | 形式 | 例 |
|---|---|---|
| 米国株 | シンボルのみ | `AAPL`, `MSFT` |
| 日本株 | `数字.T` | `7203.T` (トヨタ), `6758.T` (ソニー) |
| 為替 | `XXX=X` | `USDJPY=X` |
| ETF | シンボルのみ | `SPY`, `QQQ` |

## リファレンス

APIの詳細・利用可能なフィールド一覧 → `references/yfinance_api.md`
