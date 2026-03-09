"""
ETF 高低點追蹤 - GitHub Actions 獨立版本
每週一至五自動執行，結果提交到倉庫
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import json

# ============================================================================
# 配置
# ============================================================================

TICKERS = ['VT', 'VOO', 'VTI','SOXX']
RESULT_DIR = Path('etf_results')
TZ = pytz.timezone('Asia/Taipei')

RESULT_DIR.mkdir(exist_ok=True)

# ============================================================================
# 核心邏輯
# ============================================================================

def fetch_data(lookback_days=1095):
    """取得歷史數據"""
    end_date = datetime.now(TZ).date()
    start_date = end_date - timedelta(days=lookback_days)
    
    data = {}
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            # Flatten MultiIndex columns (newer yfinance returns MultiIndex even for single ticker)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            if df.empty or len(df) < 10:
                print(f"⚠️ {ticker} 數據不足，跳過")
                continue
            if 'Adj Close' in df.columns:
                data[ticker] = df[['Adj Close', 'High', 'Low']]
            else:
                data[ticker] = df[['Close', 'High', 'Low']].rename(columns={'Close': 'Adj Close'})
        except Exception as e:
            print(f"⚠️ {ticker} 下載失敗: {e}，跳過")
            continue
    
    return data

def calculate_metrics(data):
    """計算高低點指標"""
    results = {}
    today = datetime.now(TZ).date()
    ytd_start = datetime(today.year, 1, 1).date()
    
    windows = {
        '1M': 21,
        '3M': 63,
        '6M': 126,
        '1Y': 252,
    }
    
    for ticker, df in data.items():
        current_price = df['Adj Close'].iloc[-1]
        ticker_results = {
            '當前價格': round(current_price, 2),
            '更新時間': str(df.index[-1].date())
        }
        
        # 各時間窗口
        for window_name, days in windows.items():
            window_df = df.iloc[-days:]
            ticker_results.update(calc_window(window_df, current_price, window_name))
        
        # YTD
        ytd_df = df[df.index.date >= ytd_start]
        if len(ytd_df) > 0:
            ticker_results.update(calc_window(ytd_df, current_price, 'YTD'))
        
        # 3Y (全期)
        ticker_results.update(calc_window(df, current_price, '3Y'))
        
        results[ticker] = ticker_results
    
    return results

def calc_window(window_df, current_price, window_name):
    """計算單一窗口"""
    high = window_df['High'].max()
    high_date = window_df['High'].idxmax().date()
    low = window_df['Low'].min()
    low_date = window_df['Low'].idxmin().date()
    
    from_high = ((current_price - high) / high * 100)
    from_low = ((current_price - low) / low * 100)
    range_pct = ((high - low) / low * 100)
    
    return {
        f'H_{window_name}': round(high, 2),
        f'H_Date_{window_name}': str(high_date),
        f'From_H_%_{window_name}': round(from_high, 2),
        f'L_{window_name}': round(low, 2),
        f'L_Date_{window_name}': str(low_date),
        f'From_L_%_{window_name}': round(from_low, 2),
        f'Range_%_{window_name}': round(range_pct, 2),
    }

def plot_results(data, results):
    """生成圖表"""
    available_tickers = list(data.keys())
    n = len(available_tickers)
    if n == 0:
        print("⚠️ 無有效數據，跳過圖表生成")
        return None
    
    fig, axes = plt.subplots(n, 2, figsize=(14, 4 * n))
    if n == 1:
        axes = axes.reshape(1, -1)  # Ensure 2D shape
    fig.suptitle('ETF 高低點追蹤', fontsize=16, fontweight='bold')
    
    colors = {'VT': '#1f77b4', 'VOO': '#ff7f0e', 'VTI': '#2ca02c', 'SOXX': '#9467bd'}
    windows = ['1M', '3M', '6M', '1Y', 'YTD', '3Y']
    
    for idx, ticker in enumerate(available_tickers):
        df = data[ticker]
        
        # 價格走勢
        ax = axes[idx, 0]
        recent = df.iloc[-252:]
        ax.plot(recent.index, recent['Adj Close'], color=colors.get(ticker, '#333333'), linewidth=2)
        ax.set_title(f'{ticker} - 近一年走勢', fontweight='bold')
        ax.set_ylabel('USD')
        ax.grid(True, alpha=0.3)
        
        # 距離高低點
        ax = axes[idx, 1]
        res = results[ticker]
        
        from_high = [res.get(f'From_H_%_{w}', 0) for w in windows]
        from_low = [res.get(f'From_L_%_{w}', 0) for w in windows]
        
        x = np.arange(len(windows))
        ax.bar(x - 0.2, from_high, 0.4, label='距高點', color='#d62728', alpha=0.8)
        ax.bar(x + 0.2, from_low, 0.4, label='距低點', color='#2ca02c', alpha=0.8)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(windows)
        ax.set_title(f'{ticker} - 距離高低點 (%)', fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plot_path = RESULT_DIR / f'etf_tracker_{datetime.now(TZ).strftime("%Y%m%d")}.png'
    plt.savefig(plot_path, dpi=120, bbox_inches='tight')
    plt.close()
    
    return plot_path

def save_results(results):
    """保存結果"""
    # DataFrame
    df = pd.DataFrame(results).T
    csv_path = RESULT_DIR / f'etf_tracker_{datetime.now(TZ).strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(csv_path)
    
    # Latest CSV
    latest_csv = RESULT_DIR / 'etf_tracker_latest.csv'
    df.to_csv(latest_csv)
    
    # JSON
    json_path = RESULT_DIR / 'etf_tracker_latest.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return csv_path, json_path

def print_summary(results):
    """打印摘要"""
    print("\n" + "="*100)
    print("ETF 高低點追蹤結果")
    print("="*100)
    
    for ticker in results.keys():
        print(f"\n【{ticker}】 當前: ${results[ticker]['當前價格']:.2f}  更新: {results[ticker]['更新時間']}")
        
        for window in ['1M', '3M', '6M', '1Y', 'YTD', '3Y']:
            h = results[ticker].get(f'H_{window}')
            if h:
                h_date = results[ticker].get(f'H_Date_{window}')
                from_h = results[ticker].get(f'From_H_%_{window}')
                l = results[ticker].get(f'L_{window}')
                l_date = results[ticker].get(f'L_Date_{window}')
                from_l = results[ticker].get(f'From_L_%_{window}')
                
                print(f"  {window:>3}: H ${h:.2f} ({h_date}) {from_h:>7.2f}% | L ${l:.2f} ({l_date}) {from_l:>7.2f}%")
    
    print("\n" + "="*100 + "\n")

# ============================================================================
# 主程式
# ============================================================================

if __name__ == '__main__':
    print("🚀 開始 ETF 追蹤...\n")
    
    # 執行
    print("📊 取得數據...")
    data = fetch_data(lookback_days=1095)
    
    print("🔢 計算指標...")
    results = calculate_metrics(data)
    
    print("📈 生成圖表...")
    plot_results(data, results)
    
    print("💾 保存結果...")
    save_results(results)
    
    print_summary(results)
    
    print("✅ 完成！")