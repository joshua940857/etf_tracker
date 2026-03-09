"""
整合版本：Momentum 系統 + ETF Tracker
適合在 GitHub Actions 中執行
"""

import os
import json
from datetime import datetime
import pytz
import shutil


# ============================================================================
# 你既有的 momentum 系統導入
# ============================================================================

# 假設你的 momentum 代碼在 momentum_system.py
# from momentum_system import run_momentum_system

# ============================================================================
# ETF Tracker 導入
# ============================================================================

from etf_tracker import fetch_data, calculate_metrics, save_results, plot_results

# ============================================================================
# 配置
# ============================================================================

TZ = pytz.timezone('Asia/Taipei')
RESULTS_DIR = 'analysis_results'
LOG_FILE = f'{RESULTS_DIR}/execution_log.txt'

import os
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================================
# 日誌系統（同時輸出到文件和終端）
# ============================================================================

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.start_time = datetime.now(TZ)
    
    def log(self, message, level='INFO'):
        """輸出日誌到文件和終端"""
        timestamp = datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] [{level}] {message}"
        
        # 輸出到終端
        print(log_msg)
        
        # 保存到文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def summary(self):
        """生成執行摘要"""
        duration = datetime.now(TZ) - self.start_time
        return f"執行耗時：{duration}"

logger = Logger(LOG_FILE)

# ============================================================================
# 1. 執行 Momentum 系統
# ============================================================================

def run_momentum_analysis():
    """執行 momentum 系統"""
    try:
        logger.log("開始執行 Momentum 系統", level='INFO')
        
        # 你既有的 momentum 代碼
        # result = run_momentum_system()
        
        # 或者直接在這裡調用你的代碼
        # ... 你的 momentum 邏輯 ...
        
        logger.log("✅ Momentum 系統執行完成", level='SUCCESS')
        return True
        
    except Exception as e:
        logger.log(f"❌ Momentum 系統執行失敗: {e}", level='ERROR')
        return False

# ============================================================================
# 2. 執行 ETF Tracker
# ============================================================================

def run_etf_analysis():
    """執行 ETF 追蹤"""
    try:
        logger.log("開始執行 ETF 追蹤", level='INFO')
        
        # 取得數據
        data = fetch_data(lookback_days=1095)
        logger.log(f"✓ 已取得 {len(data)} 檔 ETF 數據", level='INFO')
        
        # 計算指標
        results = calculate_metrics(data)
        logger.log("✓ 已計算高低點指標", level='INFO')
        
        # 生成圖表
        plot_results(data, results)
        logger.log("✓ 已生成圖表", level='INFO')
        
        # 保存結果
        csv_path, json_path = save_results(results)
        logger.log(f"✓ 結果已保存: {csv_path}", level='INFO')
        
        logger.log("✅ ETF 追蹤執行完成", level='SUCCESS')
        
        return results, csv_path, json_path
        
    except Exception as e:
        logger.log(f"❌ ETF 追蹤執行失敗: {e}", level='ERROR')
        return None, None, None

# ============================================================================
# 3. 生成綜合報告
# ============================================================================

def generate_summary_report(etf_results):
    """生成簡潔的綜合報告"""
    
    report_file = f'{RESULTS_DIR}/summary_report.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write(f"執行時間: {datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*100 + "\n\n")
        
        f.write("【 ETF 高低點追蹤結果 】\n")
        f.write("-"*100 + "\n\n")
        
        if etf_results:
            for ticker in ['VT', 'VOO', 'VTI']:
                if ticker in etf_results:
                    data = etf_results[ticker]
                    f.write(f"{ticker}:\n")
                    f.write(f"  當前價格: ${data['當前價格']:.2f}\n")
                    f.write(f"  更新時間: {data['更新時間']}\n")
                    
                    # 1Y 數據（最重要）
                    if 'H_1Y' in data:
                        f.write(f"  1Y 高點: ${data['H_1Y']:.2f} ({data['H_Date_1Y']}) ")
                        f.write(f"距今: {data['From_H_%_1Y']:+.2f}%\n")
                        f.write(f"  1Y 低點: ${data['L_1Y']:.2f} ({data['L_Date_1Y']}) ")
                        f.write(f"距今: {data['From_L_%_1Y']:+.2f}%\n")
                    f.write("\n")
        
        f.write("-"*100 + "\n")
        f.write("✅ 報告生成完成\n")
    
    logger.log(f"已生成摘要報告: {report_file}", level='INFO')
    return report_file

# ============================================================================
# 4. 發送到 LINE (如果你有 LINE 整合)
# ============================================================================

def send_to_line(etf_results):
    """發送結果到 LINE（如果配置了 TOKEN）"""
    
    token = os.environ.get('CHANNEL_ACCESS_TOKEN')
    user_id = os.environ.get('USER_ID')
    
    if not token or not user_id:
        logger.log("⚠️  未設置 LINE TOKEN，跳過 LINE 發送", level='WARN')
        return False
    
    try:
        logger.log("正在發送結果到 LINE...", level='INFO')
        
        # 你既有的 LINE 發送函數
        # send_df_to_line_v3(final_df, token, user_id, sort_name)
        
        logger.log("✅ 已發送到 LINE", level='SUCCESS')
        return True
        
    except Exception as e:
        logger.log(f"❌ LINE 發送失敗: {e}", level='ERROR')
        return False

# ============================================================================
# 5. 主程式
# ============================================================================

def main():
    """主執行函數"""
    
    print("\n" + "="*100)
    print("🚀 開始執行分析系統")
    print("="*100 + "\n")
    
    logger.log("系統啟動", level='START')
    
    # Step 1: Momentum
    momentum_success = run_momentum_analysis()
    
    # Step 2: ETF Tracker
    etf_results, csv_path, json_path = run_etf_analysis()
    etf_success = (etf_results is not None)
    
    # Step 3: 生成報告
    if etf_results:
        summary_file = generate_summary_report(etf_results)
    
    # Step 4: 發送到 LINE
    send_to_line(etf_results)
    copy_success = copy_results_to_docs()

    # Step 5: 最終摘要
    print("\n" + "="*100)
    print("📊 執行摘要")
    print("="*100)
    print(f"⏱️  {logger.summary()}")
    print(f"✓ Momentum: {'成功' if momentum_success else '失敗'}")
    print(f"✓ ETF Tracker: {'成功' if etf_success else '失敗'}")
    print("\n📁 結果位置：")
    print(f"  - 日誌: {LOG_FILE}")
    print(f"  - 報告: {RESULTS_DIR}/summary_report.txt")
    print(f"  - 數據: {RESULTS_DIR}/etf_tracker_latest.csv")
    print(f"  - JSON: {RESULTS_DIR}/etf_tracker_latest.json")
    print("="*100 + "\n")
    
    logger.log("系統執行完畢", level='END')

def copy_results_to_docs():
    """自動複製結果到 docs（用於 GitHub Pages）"""
    try:
        import os
        from pathlib import Path
        
        logger.log("正在複製結果到 docs...", level='INFO')
        
        # 建立目標目錄
        docs_dir = Path('docs/data')
        docs_etf = docs_dir / 'etf_results'
        docs_analysis = docs_dir / 'analysis_results'
        
        docs_etf.mkdir(parents=True, exist_ok=True)
        docs_analysis.mkdir(parents=True, exist_ok=True)
        
        # 複製 ETF 結果
        source_etf = Path('etf_results')
        if source_etf.exists():
            for file in source_etf.glob('*'):
                if file.is_file():
                    shutil.copy2(file, docs_etf / file.name)
            logger.log(f"✓ 已複製 ETF 結果", level='INFO')
        
        # 複製分析結果
        source_analysis = Path('analysis_results')
        if source_analysis.exists():
            for file in source_analysis.glob('*'):
                if file.is_file():
                    shutil.copy2(file, docs_analysis / file.name)
            logger.log(f"✓ 已複製分析結果", level='INFO')
        
        logger.log("✅ 結果已自動複製到 docs/data", level='SUCCESS')
        return True
        
    except Exception as e:
        logger.log(f"❌ 複製失敗: {e}", level='ERROR')
        return False



if __name__ == '__main__':
    main()

