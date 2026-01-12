#!/usr/bin/env python3
import os
import sys
import datetime as dt
from typing import Dict, List

import pandas as pd
import tushare as ts


# 7个指数：上证综指、沪深300、中证500、中证1000、创业板指、上证50、深证成指
INDEXES: Dict[str, str] = {
    "上证综指": "000001.SH",
    "沪深300": "000300.SH",
    "中证500": "000905.SH",
    "中证1000": "000852.SH",
    "创业板指": "399006.SZ",
    "上证50": "000016.SH",
    "深证成指": "399001.SZ",
}


def ensure_token() -> str:
    token = os.getenv("TS_TOKEN")
    if not token:
        print("ERROR: TS_TOKEN not set. export TS_TOKEN=...")
        sys.exit(2)
    return token


def start_date_10y() -> str:
    today = dt.date.today()
    year = today.year - 10
    return f"{year}0101"


def fetch_index_daily(pro, ts_code: str, start_date: str) -> pd.DataFrame:
    df = pro.index_daily(ts_code=ts_code, start_date=start_date)
    if df is None or df.empty:
        return pd.DataFrame(columns=["trade_date", "open", "high", "low", "close"])
    df = df[["trade_date", "open", "high", "low", "close"]].copy()
    df["date"] = pd.to_datetime(df["trade_date"])  # to datetime
    df = df.sort_values("date").reset_index(drop=True)
    return df


def yearly_ohlc(daily: pd.DataFrame) -> pd.DataFrame:
    if daily.empty:
        return pd.DataFrame(columns=["year", "open", "high", "low", "close"])
    daily["year"] = daily["date"].dt.year
    # 按年份聚合：Open取当年第一天的open，Close取当年最后一天的close，High/Low取全年极值
    grouped = daily.groupby("year", sort=True)
    out = grouped.agg(
        open=("open", lambda s: float(s.iloc[0])),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", lambda s: float(s.iloc[-1])),
    ).reset_index()
    # 只保留最近10年（start_date已限制，但以防万一）
    years = sorted(out["year"].tolist())
    if len(years) > 10:
        out = out[out["year"].isin(years[-10:])]
    return out


def print_table(name: str, ts_code: str, yearly: pd.DataFrame):
    print(f"\n[指数] {name} ({ts_code}) 近10年年度OHLC：")
    if yearly.empty:
        print("数据为空")
        return
    # 格式化输出
    print("year    open      high      low       close")
    for _, row in yearly.iterrows():
        print(f"{int(row['year'])}  {row['open']:8.2f}  {row['high']:8.2f}  {row['low']:8.2f}  {row['close']:8.2f}")


def main():
    token = ensure_token()
    pro = ts.pro_api(token=token)
    start_date = start_date_10y()
    for name, code in INDEXES.items():
        try:
            daily = fetch_index_daily(pro, code, start_date)
            yearly = yearly_ohlc(daily)
            print_table(name, code, yearly)
        except Exception as e:
            print(f"[错误] {name} ({code}): {e}")


if __name__ == "__main__":
    main()

