# 🚀 GitHub Pages Web 儀表板設置指南

## 📋 概覽

我為你準備了一個**完整的 Web 儀表板**，可以在 GitHub Pages 上展示最新的分析結果。

### 包含的文件

```
docs/                          ← GitHub Pages 根目錄
├── index.html                 ← 主儀表板頁面
├── etf-detail.html            ← ETF 詳細頁面
├── about.html                 ← 關於頁面
└── data/                       ← 數據目錄（自動生成）
    ├── analysis_results/
    │   ├── summary_report.txt
    │   ├── execution_log.txt
    │   └── ...
    └── etf_results/
        ├── etf_tracker_latest.csv
        ├── etf_tracker_latest.json
        └── etf_tracker_YYYYMMDD.png
```

---

## 🎯 5 步設置

### 步驟 1：複製 HTML 文件到 docs 目錄

在你的倉庫根目錄建立 `docs` 文件夾：

```bash
mkdir -p docs
```

複製提供的 HTML 文件到 `docs/`：

```
docs/
├── index.html
├── etf-detail.html
└── about.html
```

### 步驟 2：配置 GitHub Pages

1. 進入 GitHub 倉庫 → **Settings**
2. 找到 **Pages** （左側菜單）
3. **Source** 選擇 **Deploy from a branch**
4. **Branch** 選擇 `main`（或你的主分支）
5. **Folder** 選擇 `/docs`
6. 點 **Save**

![GitHub Pages 設置](https://docs.github.com/assets/cb-33207/images/help/pages/publishing-source-dropdown.png)

### 步驟 3：更新工作流以複製結果到 docs

編輯 `.github/workflows/integrated_analysis.yml`，在 **Commit and push results** 之後添加：

```yaml
      - name: Copy results to docs
        run: |
          mkdir -p docs/data
          cp -r analysis_results docs/data/ || true
          cp -r etf_results docs/data/ || true
      
      - name: Commit and push docs
        run: |
          git add docs/data/
          git commit -m "📊 Update dashboard data" || true
          git push
```

完整的工作流改後看起來：

```yaml
      # ... 前面的步驟 ...
      
      - name: Commit and push results
        run: |
          git config user.email "action@github.com"
          git config user.name "bot"
          git add -A analysis_results/ etf_results/
          git commit -m "📊 Analysis Results: $(date +%Y-%m-%d)" || true
          git push
      
      # ← 新增以下部分
      - name: Copy results to docs
        run: |
          mkdir -p docs/data
          cp -r analysis_results docs/data/ || true
          cp -r etf_results docs/data/ || true
      
      - name: Commit and push docs
        run: |
          git add docs/data/
          git commit -m "📊 Update dashboard data" || true
          git push
      # ← 新增部分結束
      
      # ... 後面的步驟 ...
```

### 步驟 4：提交並推送

```bash
git add docs/
git add .github/workflows/integrated_analysis.yml
git commit -m "Add GitHub Pages dashboard"
git push
```

### 步驟 5：等待 GitHub Pages 部署

1. 進入 **Actions** 分頁
2. 等待工作流執行完成
3. 進入 **Settings** → **Pages**
4. 你會看到網址，例如：`https://你的用户名.github.io/你的倉庫名/`

---

## 📍 訪問你的儀表板

### URL 結構

| 頁面 | URL |
|------|-----|
| 主儀表板 | `https://你的用户名.github.io/你的倉庫名/` |
| ETF 詳細 | `https://你的用户名.github.io/你的倉庫名/etf-detail.html?ticker=VOO` |
| 關於頁面 | `https://你的用户名.github.io/你的倉庫名/about.html` |

### 例子

假設你的 GitHub 用户名是 `yuanwai`，倉庫名是 `momentum-etf`：

- 主儀表板：`https://yuanwai.github.io/momentum-etf/`
- ETF 詳細：`https://yuanwai.github.io/momentum-etf/etf-detail.html?ticker=VOO`
- 關於：`https://yuanwai.github.io/momentum-etf/about.html`

---

## 🎨 儀表板功能

### 主儀表板 (index.html)

✅ 自動載入最新數據  
✅ 實時更新（每 5 分鐘檢查一次）  
✅ 顯示三檔 ETF 的當前價格  
✅ 1Y 高點和低點的快速概覽  
✅ 點擊進入詳細頁面  
✅ 響應式設計（手機也能用）  

### 詳細頁面 (etf-detail.html)

✅ 單檔 ETF 的完整分析  
✅ 所有時間窗口的數據（1M、3M、6M、1Y、YTD、3Y）  
✅ 價格走勢圖  
✅ 彩色指示器（綠色 = 好，紅色 = 壞）  

### 關於頁面 (about.html)

✅ 系統說明  
✅ 功能介紹  
✅ 指標解釋  
✅ 常見問題  
✅ 免責聲明  

---

## 🔄 數據流

```
GitHub Actions 執行
    ↓
生成 analysis_results/ 和 etf_results/
    ↓
複製到 docs/data/
    ↓
Commit 並 push
    ↓
GitHub Pages 自動部署
    ↓
网站自動載入數據
    ↓
儀表板展示最新結果
```

---

## ⚙️ 自訂儀表板

### 改變配色

在 `index.html` 中找到 CSS 變數：

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

改為你喜歡的顏色。例如：

```css
/* 綠色系 */
background: linear-gradient(135deg, #10b981 0%, #059669 100%);

/* 藍色系 */
background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);

/* 紅色系 */
background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
```

### 添加你的 GitHub 倉庫鏈接

在 `index.html` 的 footer 中找到：

```html
<a href="https://github.com" target="_blank">GitHub 倉庫</a>
```

改為你的倉庫 URL：

```html
<a href="https://github.com/你的用户名/你的倉庫名" target="_blank">GitHub 倉庫</a>
```

### 修改執行時間說明

在 `about.html` 找到：

```html
<p>
    <strong>執行時間：</strong> 每週一至五 09:30 UTC<br>
    <strong>台北時間：</strong> 每週一至五 17:30<br>
</p>
```

改為你實際的執行時間。

---

## 🐛 常見問題

### Q: 儀表板顯示「無法載入數據」

**A:** 檢查以下幾點：

1. 工作流是否成功執行？進入 Actions 檢查
2. 數據文件是否存在？進入 `docs/data/` 查看
3. 瀏覽器控制台有錯誤嗎？按 F12 查看

### Q: 圖表不顯示

**A:** 圖表可能還沒生成。檢查：

1. `etf_results/` 目錄中是否有 `.png` 文件
2. 文件名是否正確（應該是 `etf_tracker_YYYYMMDD.png`）
3. 是否需要等待下次自動執行

### Q: 數據沒有更新

**A:** 檢查：

1. 工作流是否在定時執行？進入 Actions 查看
2. 是否有錯誤？點擊執行記錄查看日誌
3. 需要手動觸發一次嗎？Actions → Run workflow

### Q: 網站打不開

**A:** 檢查：

1. GitHub Pages 是否已啟用？Settings → Pages
2. 分支和文件夾設置是否正確？應該是 `/docs` 文件夾
3. 需要等待一會嗎？第一次部署可能需要 1-2 分鐘

### Q: 能否改變域名？

**A:** 可以：

1. 購買自己的域名
2. Settings → Pages → Custom domain
3. 按照 GitHub 的說明設置 DNS

---

## 📱 在手機上查看

儀表板已經完全響應式設計，可以在手機上正常使用：

1. 在手機上打開儀表板 URL
2. 自動適配屏幕大小
3. 所有功能都可用

---

## 🔐 隱私和安全

- ✅ 只展示公開數據（Yahoo Finance）
- ✅ 數據存儲在你自己的 GitHub 倉庫
- ✅ 沒有外部 API 調用（除了首次載入時）
- ✅ 所有代碼都開源可驗證
- ✅ HTTPS 自動啟用（GitHub Pages 默認）

---

## 🎨 進階自訂

### 添加實時通知

在 `index.html` 中添加 Slack 或 Discord webhook：

```javascript
// 執行完成時發送通知
async function notifyCompletion() {
    const webhookUrl = 'your-webhook-url';
    await fetch(webhookUrl, {
        method: 'POST',
        body: JSON.stringify({
            text: '📊 分析完成，數據已更新'
        })
    });
}
```

### 添加數據導出

在 `index.html` 中添加按鈕以導出當前數據為 CSV：

```javascript
function exportToCSV() {
    // 導出邏輯
}
```

### 添加圖表庫

整合 Chart.js 或 Plotly 以生成更豐富的圖表：

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
```

---

## 📚 更多資源

- [GitHub Pages 文檔](https://docs.github.com/en/pages)
- [HTML/CSS 教程](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [JavaScript 教程](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## ✅ 完成檢查清單

設置完成後確認：

- [ ] 已建立 `docs/` 目錄
- [ ] 三個 HTML 文件都在 `docs/` 中
- [ ] GitHub Pages 已啟用（Settings → Pages）
- [ ] 工作流已更新（添加了複製到 docs 的步驟）
- [ ] 首次執行已完成
- [ ] 網站能打開並顯示數據
- [ ] 圖表能正常加載
- [ ] 在手機上也能打開

---

## 🚀 現在就試試

1. **複製 HTML 文件** 到 `docs/` 目錄
2. **更新工作流** 以複製數據
3. **推送到 GitHub**
4. **等待部署完成**
5. **打開你的網站 URL**

就這麼簡單！🎉

---

**祝你的儀表板運行順利！** 📊✨
