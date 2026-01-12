# MktSent: 7 指数近十年年度OHLC

目标：仅输出 7 个代表性指数在最近十年的年度 OHLC（Open/High/Low/Close），用于快速查看长期趋势与波动区间。

## 依赖与配置
- 依赖：Python 3、`pandas`、`tushare`
- 环境变量：设置 Tushare 的 `TS_TOKEN`
  - macOS/Linux：`export TS_TOKEN="<your_tushare_token>"`
  - Windows(PowerShell)：`$env:TS_TOKEN = "<your_tushare_token>"`

## 指数清单（7个）
- 上证综指 `000001.SH`
- 沪深300 `000300.SH`
- 中证500 `000905.SH`
- 中证1000 `000852.SH`
- 创业板指 `399006.SZ`
- 上证50 `000016.SH`
- 深证成指 `399001.SZ`

## 使用
- 运行年度OHLC脚本：`python3 scripts/index_yearly_ohlc.py`
- 脚本行为：抓取最近十年日行情，按年聚合得到当年 `Open/High/Low/Close` 并打印结果。

