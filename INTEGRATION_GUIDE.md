# 如何整合你的 Momentum 系統

## 🎯 目標

將你的 momentum 系統和 ETF Tracker 在 GitHub Actions 中一起執行，結果都保存到倉庫。

---

## 📋 你需要準備

1. **你的 momentum_system.py**（你既有的代碼）
2. **etf_tracker.py**（已提供）
3. **integrated_analysis.py**（新增，整合層）
4. **.github/workflows/integrated_analysis.yml**（新工作流）

---

## 🚀 設置步驟

### 步驟 1：複製核心文件

在你的倉庫中應該有：

```
your-repo/
├── .github/
│   └── workflows/
│       └── integrated_analysis.yml     ← 複製此文件
├── momentum_system.py                   ← 你既有的（保留）
├── etf_tracker.py                       ← 複製此文件
└── integrated_analysis.py               ← 複製此文件
```

### 步驟 2：修改 integrated_analysis.py

打開 `integrated_analysis.py`，找到這行：

```python
# 假設你的 momentum 代碼在 momentum_system.py
# from momentum_system import run_momentum_system
```

改為：

```python
from momentum_system import run_momentum_system  # 或你的實際函數名
```

然後找到 `run_momentum_analysis()` 函數，改為：

```python
def run_momentum_analysis():
    """執行 momentum 系統"""
    try:
        logger.log("開始執行 Momentum 系統", level='INFO')
        
        # 調用你的 momentum 函數
        result = run_momentum_system()
        
        logger.log("✅ Momentum 系統執行完成", level='SUCCESS')
        return True
        
    except Exception as e:
        logger.log(f"❌ Momentum 系統執行失敗: {e}", level='ERROR')
        return False
```

### 步驟 3：修改工作流（可選）

如果你的 momentum 系統需要特殊的環境變數，編輯 `.github/workflows/integrated_analysis.yml`：

```yaml
      - name: Run analysis
        env:
          CHANNEL_ACCESS_TOKEN: ${{ secrets.CHANNEL_ACCESS_TOKEN }}
          USER_ID: ${{ secrets.USER_ID }}
          # 添加你的其他環境變數
          YOUR_VAR: ${{ secrets.YOUR_VAR }}
        run: python integrated_analysis.py
```

### 步驟 4：設置 GitHub Secrets（如果需要）

1. 進入 GitHub → **Settings** → **Secrets and variables** → **Actions**
2. 點 **New repository secret**
3. 添加你需要的 Secrets：
   - `CHANNEL_ACCESS_TOKEN` (如果有 LINE)
   - `USER_ID` (如果有 LINE)
   - 其他你的系統需要的 token

### 步驟 5：提交並推送

```bash
git add integrated_analysis.py .github/workflows/integrated_analysis.yml etf_tracker.py
git commit -m "Add integrated momentum + ETF analysis"
git push
```

---

## 📊 執行結果位置

執行完成後，倉庫中會有：

```
analysis_results/
├── execution_log.txt       ← 完整日誌（[INFO]、[ERROR] 等）
├── summary_report.txt      ← 簡潔摘要（最重要！）
└── momentum_results.csv    ← momentum 系統結果（可選）

etf_results/
├── etf_tracker_latest.csv
├── etf_tracker_latest.json
└── etf_tracker_20260309.png
```

---

## 🔍 查看結果

### 最簡單的方式

1. 進入你的 GitHub 倉庫
2. 點開 `analysis_results/` 文件夾
3. 點開 `summary_report.txt` 查看摘要

就這樣！

### 詳細查看

1. **摘要報告**：`analysis_results/summary_report.txt`
2. **完整日誌**：`analysis_results/execution_log.txt`
3. **ETF 數據**：`etf_results/etf_tracker_latest.csv`
4. **ETF 圖表**：`etf_results/etf_tracker_20260309.png`

### 在 GitHub Actions 中看實時輸出

1. 進入 GitHub → **Actions**
2. 點最新的執行記錄
3. 點 **Run analysis** 展開
4. 看所有 print() 輸出

---

## 💡 你的 momentum 系統代碼放哪裡？

### 選項 A：保持原樣（推薦）

你的 `momentum_system.py` 保持不變，`integrated_analysis.py` 會調用它。

優點：
- ✅ 改動最少
- ✅ 兩個系統獨立
- ✅ 易於維護

### 選項 B：直接集成

如果你的代碼比較簡單，可以直接寫在 `integrated_analysis.py` 中。

改這部分：

```python
def run_momentum_analysis():
    """執行 momentum 系統"""
    try:
        logger.log("開始執行 Momentum 系統", level='INFO')
        
        # ===== 直接寫你的 momentum 代碼 =====
        # ... 你的代碼 ...
        # final_df = ...
        # token = os.environ.get('CHANNEL_ACCESS_TOKEN')
        # user_id = os.environ.get('USER_ID')
        # send_df_to_line_v3(final_df, token, user_id, sort_name)
        # =====================================
        
        logger.log("✅ Momentum 系統執行完成", level='SUCCESS')
        return True
        
    except Exception as e:
        logger.log(f"❌ Momentum 系統執行失敗: {e}", level='ERROR')
        return False
```

---

## 🐛 常見問題

### Q: 怎樣知道程式是否成功執行？

**A:** 三個地方可以看：

1. **GitHub Actions** → 綠色 ✅ = 成功，紅色 ❌ = 失敗
2. **倉庫中的文件** → 有新的 `summary_report.txt` = 成功
3. **日誌文件** → 看 [SUCCESS] 或 [ERROR]

### Q: 執行失敗了怎麼辦？

**A:** 按順序檢查：

1. 進入 GitHub Actions，看紅色 ❌ 的步驟
2. 展開看詳細錯誤信息
3. 或打開 `execution_log.txt` 找 [ERROR] 行
4. 根據錯誤信息修改代碼

### Q: 能不能跳過 momentum，只執行 ETF？

**A:** 可以，改 `integrated_analysis.py`：

```python
def main():
    # 注釋掉這行
    # momentum_success = run_momentum_analysis()
    momentum_success = True  # 假裝成功
    
    # 只執行 ETF
    etf_results, csv_path, json_path = run_etf_analysis()
    ...
```

### Q: 每次執行時間多久？

**A:** 通常 2-3 分鐘，包括：
- 下載數據：1 分鐘
- 執行分析：1 分鐘
- 上傳結果：30 秒

### Q: 結果會一直累積嗎？

**A:** 會的。如果想定期清理老文件：

```bash
# 刪除超過 30 天的文件
find analysis_results -type f -mtime +30 -delete
```

---

## 🎯 下一步

1. **現在就試試**：按上面的步驟設置
2. **推送到 GitHub**：`git push`
3. **等待自動執行**：等下個定時時間（或手動執行）
4. **查看結果**：進倉庫打開 `summary_report.txt`

---

## 📞 需要幫助？

- **日誌去哪裡了？** → 見 `GITHUB_LOGS_GUIDE.md`
- **怎樣改執行時間？** → 編輯 cron 時間（見 ETF_TRACKER_GUIDE.md）
- **想添加通知？** → 見進階部分

---

**現在你知道怎樣整合你的系統了！** 🚀
