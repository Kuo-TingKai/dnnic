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
** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** test_mac.mac_test_basic        PASS           1.00           0.00       2398.12  **
** test_mac.mac_test_max_values   PASS           1.00           0.00       8701.88  **
** test_mac.mac_test_random       PASS          10.00           0.00      19004.55  **
** test_mac.mac_test_edge_cases   PASS           2.00           0.00       9845.78  **
** TESTS=4 PASS=4 FAIL=0 SKIP=0                 14.00           0.00       6198.72  **
```

## 合成結果與視覺化

### 閘級網表統計
執行 `make synth` 後，Yosys 會產生詳細的合成報告：

```
=== mac_unit ===
        +----------Local Count, excluding submodules.
        | 
      872 wires
      916 wire bits
        4 public wires
       48 public wire bits
        4 ports
       48 port bits
      412 cells
        8   $_ANDNOT_
       85   $_AND_
      164   $_NAND_
        1   $_NOR_
       14   $_OR_
       34   $_XNOR_
      106   $_XOR_
```

### 合成後的閘級網表
合成後的 `mac_unit_synth.v` 包含：
- **412 個邏輯閘**：包含 AND、NAND、XOR、XNOR 等基本邏輯閘
- **872 條內部連線**：連接各個邏輯閘
- **48 個 I/O 位元**：8+8+16+16 = 48 位元的輸入輸出

### 電路架構視覺化
MAC 單元的邏輯結構：

```
    A[7:0] ──┐
             │
             ├─→ 8×8 乘法器 ──┐
             │                │
    W[7:0] ──┘                │
                               ├─→ 16位元加法器 ──→ C[15:0]
                               │
    B[15:0] ──────────────────┘
```

### 合成優化結果
- **乘法器優化**：8×8 乘法器被優化為 412 個基本邏輯閘
- **加法器優化**：16位元加法器使用進位傳播加法器結構
- **面積效率**：總共使用 412 個邏輯閘實現完整的 MAC 功能

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

## DNN 加速器擴展

### 完整 DNN 加速器架構
本專案已擴展為完整的 2 層神經網路加速器：

```
輸入層 (4 個輸入) → 隱藏層 (3 個神經元) → 輸出層 (2 個輸出)
```

### DNN 加速器特色
- **狀態機控制**: 自動化運算流程
- **權重儲存**: 內建權重和偏置記憶體
- **時鐘同步**: 完整的時鐘域設計
- **控制信號**: start、done、valid 信號

### DNN 加速器使用方式

1. **測試 DNN 加速器**:
   ```bash
   source venv/bin/activate
   make test-dnn
   ```

2. **合成 DNN 加速器**:
   ```bash
   make synth-dnn
   ```

### DNN 加速器架構圖
```
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   輸入層    │    │   隱藏層    │    │   輸出層    │
    │ 4 個輸入    │───▶│ 3 個神經元  │───▶│ 2 個輸出    │
    └─────────────┘    └─────────────┘    └─────────────┘
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   MAC 單元  │    │   MAC 單元  │    │   MAC 單元  │
    │ 4×3 權重    │    │ 3×2 權重    │    │ 偏置加法    │
    └─────────────┘    └─────────────┘    └─────────────┘
```

### DNN 加速器測試結果
```
** TEST                                     STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
** test_dnn.dnn_test_basic_functionality     PASS         230.00           0.00     280107.41  **
** test_dnn.dnn_test_multiple_computations   PASS         440.00           0.00     477365.17  **
** test_dnn.dnn_test_state_machine           PASS         230.00           0.00     672726.58  **
** test_dnn.dnn_test_edge_cases              PASS         440.00           0.00     333001.40  **
** test_dnn.dnn_test_random_inputs           PASS        1080.00           0.00     787936.74  **
** TESTS=5 PASS=5 FAIL=0 SKIP=0                          2420.00           0.01     367176.69  **
```

### DNN 加速器合成結果
執行 `make synth-dnn` 後，Yosys 會產生詳細的合成報告：

```
=== dnn_accelerator ===
        +----------Local Count, excluding submodules.
        | 
     1425 wires
     1796 wire bits
       45 public wires
      396 public wire bits
       15 ports
      117 port bits
      671 cells
       25   $_ANDNOT_
      132   $_AND_
       24   $_DFFE_PN0P_
       32   $_DFFE_PP_
       27   $_MUX_
      228   $_NAND_
        7   $_NOR_
        9   $_NOT_
       17   $_ORNOT_
       24   $_OR_
       41   $_XNOR_
      105   $_XOR_
        1 submodules
        1   mac_unit
```

### DNN 加速器合成後的閘級網表
合成後的 `dnn_accelerator_synth.v` 包含：
- **671 個邏輯閘**：包含 AND、NAND、XOR、XNOR、MUX、DFF 等基本邏輯閘
- **1425 條內部連線**：連接各個邏輯閘
- **117 個 I/O 位元**：時鐘、重置、控制信號和資料輸入輸出
- **1 個子模組**：內嵌的 MAC 單元

## 軟硬體一致性驗證

本專案實現了完整的軟硬體 DNN 一致性驗證流程：

### 1. 軟體 DNN 訓練
使用 PyTorch 訓練一個小型 2 層神經網路：
```bash
make train-model
```

**訓練結果**：
- 測試準確率：79.5%
- 模型架構：4 輸入 → 3 隱藏神經元 → 2 輸出
- 參數數量：18 個權重 + 5 個偏置

### 2. 參數轉換
將軟體模型參數轉換為硬體相容格式：
```bash
make convert-params
```

**轉換結果**：
- Layer 1 權重：4×3 矩陣，8 位元整數
- Layer 1 偏置：3 個值，16 位元整數
- Layer 2 權重：3×2 矩陣，8 位元整數
- Layer 2 偏置：2 個值，16 位元整數

### 3. 硬體 DNN 加速器
實作可配置的硬體 DNN 加速器：
- 支援動態參數載入
- 狀態機控制計算流程
- MAC 單元並行運算

### 4. 一致性驗證
比較軟體和硬體 DNN 的輸出結果：
```bash
python3 verify_consistency.py
```

**驗證結果**：
```
=== Software-Hardware DNN Consistency Verification ===
Loaded 10 test vectors

Test 1: Input=[70, 120, 201, 51]
  Software: [104450.00, 72861.00]
  Hardware: [104450.00, 72861.00]
  Difference: [    0.00,     0.00] ✅ PASS

Test 2: Input=[65, 64, 127, 96]
  Software: [   59.00,   -47.00]
  Hardware: [   59.00,   -47.00]
  Difference: [    0.00,     0.00] ✅ PASS

... (所有 10 個測試案例)

=== Summary ===
Maximum difference across all tests: 0.000000
✅ ALL TESTS PASSED - Software and hardware outputs are consistent!
```

### 5. 完整流程
執行完整的訓練和驗證流程：
```bash
make full-pipeline
```

這將依序執行：
1. 軟體模型訓練
2. 參數轉換
3. 硬體測試
4. 一致性驗證

## 進一步擴展建議

1. **增加層數**: 擴展為多層深度神經網路
2. **並行處理**: 實作多個 MAC 單元並行運算
3. **記憶體介面**: 增加外部記憶體存取權重和資料
4. **激活函數**: 加入 ReLU、Sigmoid 等激活函數
5. **量化支援**: 支援不同位元寬度的量化運算
6. **流水線設計**: 增加暫存器來提高時鐘頻率

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
