#!/usr/bin/env python3
"""
株価収集スクリプト (Stock Price Collector)

yfinanceを使って株価データを取得するユーティリティ。
Usage:
    python fetch_stock.py --mode current --symbols AAPL MSFT
    python fetch_stock.py --mode history --symbols AAPL --period 1mo
    python fetch_stock.py --mode info --symbols AAPL MSFT
    python fetch_stock.py --mode batch --symbols AAPL MSFT GOOG --mode current
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance is not installed. Run: pip install yfinance")
    sys.exit(1)


def get_current_price(symbol: str) -> dict:
    """現在株価を取得する。"""
    ticker = yf.Ticker(symbol)
    info = ticker.fast_info
    hist = ticker.history(period="2d")

    if hist.empty:
        return {"symbol": symbol, "error": "データなし"}

    latest = hist.iloc[-1]
    prev = hist.iloc[-2] if len(hist) > 1 else hist.iloc[-1]
    change = latest["Close"] - prev["Close"]
    change_pct = (change / prev["Close"]) * 100

    return {
        "symbol": symbol,
        "price": round(float(latest["Close"]), 2),
        "open": round(float(latest["Open"]), 2),
        "high": round(float(latest["High"]), 2),
        "low": round(float(latest["Low"]), 2),
        "volume": int(latest["Volume"]),
        "change": round(float(change), 2),
        "change_pct": round(float(change_pct), 2),
        "date": latest.name.strftime("%Y-%m-%d"),
    }


def get_history(symbol: str, period: str = "1mo", interval: str = "1d") -> dict:
    """過去の株価データを取得する。

    period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)

    if hist.empty:
        return {"symbol": symbol, "error": "データなし"}

    records = []
    for date, row in hist.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d %H:%M" if interval not in ("1d", "5d", "1wk", "1mo", "3mo") else "%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]),
        })

    return {
        "symbol": symbol,
        "period": period,
        "interval": interval,
        "count": len(records),
        "data": records,
    }


def get_financials(symbol: str) -> dict:
    """財務指標・基本情報を取得する。"""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    fields = {
        "symbol": symbol,
        "name": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "currency": info.get("currency"),
        "exchange": info.get("exchange"),
        # バリュエーション
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "ps_ratio": info.get("priceToSalesTrailing12Months"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        # 配当
        "dividend_yield": info.get("dividendYield"),
        "dividend_rate": info.get("dividendRate"),
        "payout_ratio": info.get("payoutRatio"),
        # 収益性
        "profit_margin": info.get("profitMargins"),
        "operating_margin": info.get("operatingMargins"),
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        # 成長
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        # アナリスト
        "target_price": info.get("targetMeanPrice"),
        "recommendation": info.get("recommendationKey"),
        # 52週高値/安値
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "50d_avg": info.get("fiftyDayAverage"),
        "200d_avg": info.get("twoHundredDayAverage"),
    }

    # Noneを除外
    return {k: v for k, v in fields.items() if v is not None}


def batch_fetch(symbols: list, mode: str = "current", **kwargs) -> list:
    """複数銘柄を一括取得する。"""
    results = []
    for symbol in symbols:
        try:
            if mode == "current":
                results.append(get_current_price(symbol))
            elif mode == "history":
                results.append(get_history(symbol, **kwargs))
            elif mode == "info":
                results.append(get_financials(symbol))
        except Exception as e:
            results.append({"symbol": symbol, "error": str(e)})
    return results


def main():
    parser = argparse.ArgumentParser(description="株価収集ツール")
    parser.add_argument("--symbols", nargs="+", required=True, help="ティッカーシンボル (例: AAPL MSFT)")
    parser.add_argument("--mode", choices=["current", "history", "info", "batch"], default="current",
                        help="取得モード: current=現在価格, history=履歴, info=財務情報, batch=一括")
    parser.add_argument("--period", default="1mo", help="履歴期間 (例: 1d, 5d, 1mo, 3mo, 1y, max)")
    parser.add_argument("--interval", default="1d", help="データ間隔 (例: 1m, 1h, 1d, 1wk, 1mo)")
    parser.add_argument("--output", choices=["json", "table"], default="json", help="出力形式")
    args = parser.parse_args()

    symbols = [s.upper() for s in args.symbols]

    if args.mode == "current":
        results = [get_current_price(s) for s in symbols]
    elif args.mode == "history":
        results = [get_history(s, period=args.period, interval=args.interval) for s in symbols]
    elif args.mode == "info":
        results = [get_financials(s) for s in symbols]
    elif args.mode == "batch":
        results = batch_fetch(symbols, mode="current")

    if args.output == "json":
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=2))
    else:
        # テーブル形式（currentモードのみ）
        if args.mode == "current":
            print(f"{'Symbol':<8} {'Price':>10} {'Change':>8} {'Change%':>8} {'Volume':>12} {'Date'}")
            print("-" * 60)
            for r in results:
                if "error" not in r:
                    print(f"{r['symbol']:<8} {r['price']:>10.2f} {r['change']:>+8.2f} {r['change_pct']:>+7.2f}% {r['volume']:>12,} {r['date']}")
                else:
                    print(f"{r['symbol']:<8} ERROR: {r['error']}")


if __name__ == "__main__":
    main()
