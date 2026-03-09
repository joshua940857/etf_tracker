# GitHub Actions 中的日誌和結果查看

## 🤔 問題：在 GitHub 執行後，print() 會輸出到哪裡？

答案：
1. **工作流日誌** - 在 Actions 分頁看到
2. **結果文件** - 保存到倉庫中
3. **Artifacts** - 保留 30 天的執行成果

---

## 📍 三個地方可以查看結果

### 1️⃣ GitHub Actions 日誌（實時）

執行過程中的 `print()` 會出現在這裡。

**如何查看：**

1. 進入 GitHub → **Actions** 分頁
2. 點擊最新的執行記錄
3. 點擊 **Run analysis** 步驟
4. 展開看詳細輸出

```
📍 位置：
GitHub → Actions → [執行記錄] → Run analysis → 展開看輸出
```

**缺點：**
- 只能看實時輸出（print）
- 關閉後難以回查
- 訊息很多，不好找關鍵信息

---

### 2️⃣ 倉庫中的結果文件（推薦）✅

執行完成後，所有結果會被提交到倉庫中的文件。

**位置：**

```
analysis_results/
├── execution_log.txt      ← 完整執行日誌
├── summary_report.txt     ← 摘要報告（最重要！）
└── ...其他文件

etf_results/
├── etf_tracker_latest.csv
├── etf_tracker_latest.json
└── etf_tracker_20260309.png
```

**如何查看：**

1. 進入你的 GitHub 倉庫主頁
2. 點擊進入 `analysis_results/` 文件夾
3. 點擊 `summary_report.txt` 查看摘要
4. 點擊 `execution_log.txt` 查看詳細日誌

**優點：**
- ✅ 永久保存
- ✅ 容易找
- ✅ 可以比較歷史

---

### 3️⃣ GitHub Artifacts（臨時備份）

每次執行的完整結果會被保存 30 天。

**如何查看：**

1. 進入 GitHub → **Actions**
2. 點擊最新的執行記錄
3. 向下滾動到 **Artifacts** 部分
4. 點擊 `analysis-results-xxx` 下載

---

## 🎯 推薦的使用方式

### 日常查看（簡單）

1. 進入倉庫
2. 打開 `analysis_results/summary_report.txt`
3. 看摘要，完成！

### 詳細檢查

1. 打開 `analysis_results/execution_log.txt` 看詳細日誌
2. 打開 `etf_results/etf_tracker_latest.csv` 看完整數據
3. 打開 `etf_results/etf_tracker_latest.png` 看圖表

### 故障排除

1. 進入 GitHub Actions 日誌
2. 找紅色的 ❌ 步驟
3. 展開看詳細輸出
4. 或查看 `execution_log.txt` 找 [ERROR] 行

---

## 📄 日誌文件格式說明

### summary_report.txt（摘要報告）

```
====================================
執行時間: 2026-03-09 17:35:42
====================================

【 ETF 高低點追蹤結果 】
------------------------------------

VT:
  當前價格: $123.45
  更新時間: 2026-03-09
  1Y 高點: $125.67 (2026-02-15) 距今: -1.76%
  1Y 低點: $120.00 (2025-10-20) 距今: +2.88%

VOO:
  當前價格: $507.32
  ...

✅ 報告生成完成
```

### execution_log.txt（詳細日誌）

```
[2026-03-09 17:30:00] [START] 系統啟動
[2026-03-09 17:30:01] [INFO] 開始執行 Momentum 系統
[2026-03-09 17:31:30] [SUCCESS] ✅ Momentum 系統執行完成
[2026-03-09 17:31:31] [INFO] 開始執行 ETF 追蹤
[2026-03-09 17:31:45] [INFO] ✓ 已取得 3 檔 ETF 數據
[2026-03-09 17:31:46] [INFO] ✓ 已計算高低點指標
...
[2026-03-09 17:33:00] [END] 系統執行完畢
```

---

## 🔄 完整的信息流

```
GitHub Actions 執行
  ↓
程式 print() 輸出 → Actions 日誌頁面
  ↓
日誌保存到文件 → analysis_results/execution_log.txt
  ↓
結果保存到文件 → etf_results/ 和 analysis_results/
  ↓
git add 並 commit → 提交到倉庫
  ↓
你在倉庫中看到更新
```

---

## 💡 最佳實踐

### 推薦做法

1. **設置時，檢查日誌**
   - 進入 Actions 看實時輸出
   - 確保沒有紅色 ❌

2. **定期檢查結果**
   - 每週查看一次 `summary_report.txt`
   - 或設置郵件通知

3. **查看詳細數據**
   - 在 `etf_results/etf_tracker_latest.csv` 中查看
   - 用 Excel 或 Google Sheets 打開

### 不推薦

❌ 依賴 print() 輸出看結果
❌ 經常進 Actions 日誌看詳細信息
❌ 只在 GitHub 網頁查看（應該 git pull 到本地）

---

## 🚨 常見問題

### Q: 執行失敗了，我怎樣看錯誤信息？

**A:** 
1. 進入 Actions → 最新執行 → 點展開失敗的步驟
2. 或查看 `execution_log.txt` 找 [ERROR]
3. 通常能看到具體是哪步出錯

### Q: 能不能直接看 print() 的輸出？

**A:** 可以，在 Actions 日誌中：
1. 進入執行記錄
2. 點 **Run analysis** 步驟
3. 展開看所有 print() 輸出

但這不是最好的方式，因為：
- 混雜著系統日誌，難找
- GitHub Actions 有日誌大小限制
- 更新或查看都不方便

**更好的方式：** 用文件存儲（已幫你設置）

### Q: 倉庫中的文件會一直累積嗎？

**A:** 會的。如果想定期清理：

```bash
# 定期刪除舊的執行結果
find analysis_results -type f -mtime +30 -delete
```

或改工作流，只保留最新的一個

### Q: 怎樣下載所有結果？

**A:** 兩個方法：

**方法 1：從倉庫 Clone（推薦）**
```bash
git clone https://github.com/你的名字/你的倉庫.git
cd 你的倉庫
# 所有結果都在本地
```

**方法 2：從 Artifacts 下載**
1. 進入 Actions
2. 點執行記錄
3. 向下找 Artifacts
4. 下載

---

## 📊 改進建議

### 想進一步優化？

1. **添加郵件通知**
   - 每次執行完，發送摘要到你的郵箱

2. **自動上傳到雲端**
   - 結果上傳到 Google Drive 或 Dropbox

3. **建立 Web 儀表板**
   - 用 GitHub Pages 展示最新結果

4. **Slack 通知**
   - 執行完後發送到 Slack

這些都可以在工作流中配置，有需要我再幫你設置。

---

## ✅ 總結

| 查看位置 | 用途 | 如何存取 |
|---------|------|---------|
| **GitHub Actions 日誌** | 即時監控、故障排除 | Actions → 執行記錄 → 展開步驟 |
| **倉庫中的文件** | 日常檢查、歷史保存 | 倉庫主頁 → analysis_results/ |
| **Artifacts** | 臨時備份、手動下載 | Actions → 執行記錄 → Artifacts |

**最常用的：倉庫中的 `summary_report.txt`**

---

**現在你知道在 GitHub 執行後訊息會去哪裡了！** 🎉
