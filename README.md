# 最簡單的 DNN 電路範例專案

這是一個基於開源工具鏈的最簡單 DNN（深度神經網路）電路實作範例，使用 MAC（乘法累加）單元作為核心元件。

## 專案結構

```
dnnic/
├── mac_unit.v          # MAC 單元的 Verilog 實作
├── test_mac.py         # cocotb 測試程式
├── Makefile            # 測試和合成配置
├── synth.ys            # Yosys 合成腳本
├── mac_unit.pcf        # FPGA 約束檔案
└── README.md           # 本說明文件
```

## 功能說明

MAC 單元是 DNN 加速器的核心元件，執行 `C = A × W + B` 運算：
- **A**: 8位元輸入資料
- **W**: 8位元權重
- **B**: 16位元偏置或累積值
- **C**: 16位元輸出結果

## 環境需求

### 必要工具
- **Python 3.6+**
- **cocotb**: Python 測試框架
- **Verilator**: 開源 Verilog 模擬器
- **Yosys**: 開源邏輯合成工具

### 安裝指令

```bash
# 安裝 Python 依賴
pip install cocotb

# 安裝 Verilator (macOS)
brew install verilator

# 安裝 Yosys (macOS)
brew install yosys
```

## 使用方式

### 1. 功能驗證

執行 cocotb 測試來驗證 MAC 單元的功能：

```bash
make
```

這會執行以下測試：
- 基本功能測試：`(10 × 2 + 5) = 25`
- 最大值測試：`(255 × 255 + 0) = 65025`
- 隨機值測試：10 組隨機輸入
- 邊界條件測試：零乘法和零偏置

### 2. 邏輯合成

使用 Yosys 將 Verilog 程式碼合成為閘級網表：

```bash
make synth
```

這會產生：
- `mac_unit_synth.v`: 合成後的 Verilog 網表
- `mac_unit.json`: JSON 格式的網表（用於 FPGA 流程）

### 3. 完整 FPGA 流程（進階）

如果您有 iCE40 FPGA 開發板，可以執行完整的 FPGA 流程：

```bash
# 合成（產生 JSON 網表）
yosys -p 'synth_ice40 -top mac_unit -json mac_unit.json' mac_unit.v

# 佈局繞線
nextpnr-ice40 --hx1k --json mac_unit.json --pcf mac_unit.pcf --asc mac_unit.asc --freq 25

# 產生位元流
icepack mac_unit.asc mac_unit.bin

# 燒錄到 FPGA
iceprog mac_unit.bin
```

## 測試結果範例

成功的測試輸出應該類似：

```
mac_test_basic (PASS)
mac_test_max_values (PASS)
mac_test_random (PASS)
mac_test_edge_cases (PASS)
```

## 檔案說明

### `mac_unit.v`
- MAC 單元的 Verilog 實作
- 8位元 × 8位元乘法器
- 16位元加法器
- 純組合邏輯設計

### `test_mac.py`
- 使用 cocotb 撰寫的測試程式
- 包含多種測試案例
- 自動化驗證功能正確性

### `Makefile`
- cocotb 測試配置
- 合成目標
- 清理目標

### `synth.ys`
- Yosys 合成腳本
- 優化設定
- 輸出格式配置

### `mac_unit.pcf`
- FPGA 約束檔案
- 引腳對應設定
- 適用於 iCE40 FPGA

## 擴展建議

1. **增加時鐘域**: 將 MAC 單元改為同步設計
2. **流水線設計**: 增加暫存器來提高時鐘頻率
3. **多個 MAC 單元**: 實作陣列處理器
4. **記憶體介面**: 增加權重和資料的記憶體存取
5. **控制邏輯**: 增加狀態機來控制運算流程

## 故障排除

### 常見問題

1. **cocotb 安裝失敗**
   ```bash
   pip install --upgrade pip
   pip install cocotb
   ```

2. **Verilator 找不到**
   ```bash
   export PATH="/opt/homebrew/bin:$PATH"
   ```

3. **Yosys 合成錯誤**
   - 檢查 Verilog 語法
   - 確認模組名稱正確

### 清理檔案

```bash
make clean          # 清理測試檔案
make clean-all      # 清理所有檔案
```

## 參考資料

- [cocotb 官方文件](https://docs.cocotb.org/)
- [Yosys 官方文件](https://yosyshq.net/yosys/)
- [Project IceStorm](https://github.com/YosysHQ/icestorm)
- [Nextpnr](https://github.com/YosysHQ/nextpnr)

## 授權

本專案使用 MIT 授權條款。
