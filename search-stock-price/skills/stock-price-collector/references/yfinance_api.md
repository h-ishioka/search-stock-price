# yfinance APIリファレンス

## インストール

```bash
pip install yfinance
```

## 基本的な使い方

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
```

## 現在・直近データ

```python
# fast_info (軽量・高速)
info = ticker.fast_info
info.last_price        # 最新価格
info.market_cap        # 時価総額
info.fifty_day_average # 50日移動平均

# 直近2日の履歴から前日比を計算
hist = ticker.history(period="2d")
latest = hist.iloc[-1]
prev   = hist.iloc[-2]
change_pct = (latest["Close"] - prev["Close"]) / prev["Close"] * 100
```

## 履歴データ

```python
# period: 1d 5d 1mo 3mo 6mo 1y 2y 5y 10y ytd max
# interval: 1m 2m 5m 15m 30m 60m 90m 1h 1d 5d 1wk 1mo 3mo
hist = ticker.history(period="1mo", interval="1d")
# 返り値: DataFrame (Open High Low Close Volume Dividends Stock Splits)
```

## 財務情報 (ticker.info)

よく使うキー一覧:

| カテゴリ | キー | 説明 |
|---|---|---|
| 基本 | longName / shortName | 会社名 |
| 基本 | sector / industry | セクター・業種 |
| 基本 | currency / exchange | 通貨・取引所 |
| 価格 | currentPrice | 現在価格 |
| 価格 | fiftyTwoWeekHigh / Low | 52週高値・安値 |
| 価格 | fiftyDayAverage | 50日移動平均 |
| 価格 | twoHundredDayAverage | 200日移動平均 |
| バリュエーション | trailingPE / forwardPE | PER（実績/予想） |
| バリュエーション | priceToBook | PBR |
| バリュエーション | priceToSalesTrailing12Months | PSR |
| バリュエーション | enterpriseToEbitda | EV/EBITDA |
| 配当 | dividendYield | 配当利回り |
| 配当 | dividendRate | 年間配当額 |
| 配当 | payoutRatio | 配当性向 |
| 収益性 | profitMargins | 純利益率 |
| 収益性 | operatingMargins | 営業利益率 |
| 収益性 | returnOnEquity | ROE |
| 収益性 | returnOnAssets | ROA |
| 成長 | revenueGrowth | 売上成長率 |
| 成長 | earningsGrowth | 利益成長率 |
| アナリスト | targetMeanPrice | 目標株価（平均） |
| アナリスト | recommendationKey | buy/hold/sell |
| アナリスト | numberOfAnalystOpinions | アナリスト数 |

## 複数銘柄の一括取得

```python
# download()で複数銘柄の履歴を一括取得
df = yf.download(["AAPL", "MSFT", "GOOG"], period="1mo")
# MultiIndex DataFrame: (Open/High/Low/Close/Volume, Symbol)

# 各銘柄の終値だけ取り出す
closes = df["Close"]  # 列がティッカーシンボル
```

## 注意事項

- `ticker.info` はフルAPIコールで遅い。価格だけなら `fast_info` か `history()` を使う
- レート制限に注意。多数銘柄を取得する場合は `yf.download()` を使うと効率的
- 日本株は `7203.T`（トヨタ）のようにサフィックス `.T` を付ける
- 為替は `USDJPY=X` のような形式
- 市場時間外はリアルタイム価格が取得できない場合がある

## ティッカーシンボル例

| 銘柄 | シンボル |
|---|---|
| Apple | AAPL |
| Microsoft | MSFT |
| Alphabet (Google) | GOOG / GOOGL |
| Amazon | AMZN |
| NVIDIA | NVDA |
| Tesla | TSLA |
| トヨタ | 7203.T |
| ソニー | 6758.T |
| USD/JPY | USDJPY=X |
| S&P 500 ETF | SPY |
| 日経平均ETF | EWJ |
