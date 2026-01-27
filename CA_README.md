# 元胞自动机 (CA) 博物馆疏散模拟系统

## 概述

这是一个基于**离散网格的元胞自动机(Cellular Automaton)**的博物馆疏散模拟系统。系统通过Excel配置、Python仿真和数据分析，实现了一个完整的大规模人员疏散模型。

### 主要特性

- ✅ **100×100离散网格** - 经典元胞自动机架构
- ✅ **8邻域移动** - 更逼真的人员流动（8个方向）
- ✅ **冲突解决** - 多人目标同一格子时的优先级处理
- ✅ **age-based行为** - 儿童、老年人有特殊处理
- ✅ **恐慌传播** - 周围恐慌等级影响个体
- ✅ **Excel配置** - 直观编辑博物馆布局
- ✅ **完整输出** - Excel报表、CSV日志、热力图

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如果尚未安装 `openpyxl`：
```bash
pip install openpyxl
```

### 2. 运行演示

无需配置文件，直接测试系统：
```bash
python test_ca_demo.py
```

这会生成一个100×100的网格、75个随机放置的代理、4个出口，并运行疏散模拟。

### 3. 创建自定义配置

```bash
python setup_ca.py
```

这会在 `config/museum_ca_config.xlsx` 创建一个空模板。

### 4. 编辑配置

在Excel中打开 `config/museum_ca_config.xlsx`：

| 值 | 含义 |
|----|------|
| 0 | 空单元格 |
| 2 | 墙体障碍 |
| 3 | 出口 |
| 4 | 入口 |
| 5 | 普通展品 |
| 6 | 特殊展品 |
| 7 | 安保人员 |

在前100×100行编辑网格。在102-106行设置参数：
- 102: 模拟步数 (默认1000)
- 103: 初始人数 (默认75)
- 104: 恐慌传播率 (默认0.05)
- 105: 恐慌衰减率 (默认0.01)
- 106: 拥挤阈值 (默认5)

### 5. 运行完整模拟

```bash
python main_ca.py
```

结果会保存到 `output/` 目录：
- `ca_simulation_results.xlsx` - 完整Excel报表
- `ca_simulation_log.csv` - 详细代理轨迹
- `ca_statistics.csv` - 时步统计
- `ca_heatmap.png` - 拥挤和恐慌热力图

---

## 系统架构

### 模块结构

```
Night_at_Museum/
├── core/ca/                        # 核心CA仿真模块
│   ├── __init__.py
│   ├── ca_grid.py                 # 双层网格管理
│   ├── ca_agent.py                # 离散网格代理
│   ├── ca_environment.py          # 静态环境管理
│   ├── ca_behaviors.py            # 8邻域移动与冲突解决
│   └── ca_engine.py               # 仿真主循环
│
├── io/                             # Excel I/O模块
│   ├── __init__.py
│   ├── excel_parser.py            # 读取Excel配置
│   └── excel_writer.py            # 写入Excel结果
│
├── analysis/
│   ├── ca_logger.py               # CA专用日志记录
│   └── (其他现有文件)
│
├── config/
│   ├── ca_settings.py             # CA专用配置参数
│   ├── museum_ca_config.xlsx      # 用户配置文件（自动生成）
│   └── (其他现有文件)
│
├── main_ca.py                      # CA仿真主入口
├── test_ca_demo.py                # 演示和测试脚本
├── setup_ca.py                    # 初始化脚本
└── requirements.txt               # 依赖包列表
```

### 核心类详解

#### CAGrid - 双层网格
```python
from core.ca import CAGrid

grid = CAGrid(100, 100)
grid.set_cell_type(10, 10, CELL_WALL)  # 添加墙
grid.place_agent(agent_id=0, x=50, y=50)  # 放置代理
neighbors = grid.get_neighbors_8(50, 50)  # 获取8邻域
```

#### CAAgent - 代理
```python
from core.ca import CAAgent

agent = CAAgent(agent_id=0, x=50, y=50, age=30, family_id=1)
agent.panic_level  # 0.0-1.0
agent.update_panic(nearby_panic=0.3, danger_proximity=0.1)
agent.evacuated  # 是否已疏散
```

#### CASimulation - 仿真引擎
```python
from core.ca import CASimulation

sim = CASimulation(100, 100, max_timesteps=1000)
sim.add_agent(0, 50, 50, age=30)
sim.environment.add_exit(95, 50)

for step in range(1000):
    sim.step()
    if len([a for a in sim.agents if not a.evacuated]) == 0:
        break
```

#### CALogger - 日志记录
```python
from analysis.ca_logger import CALogger

logger = CALogger()

for step in range(1000):
    sim.step()
    logger.log_step(step, sim.agents, sim.grid, sim.get_statistics())

df = logger.save_to_csv("output/log.csv")
heatmap = logger.get_crowding_heatmap(100, 100)
```

---

## 8邻域移动规则

### 邻域定义
```
[NW] [N ] [NE]     (-1,-1) (0,-1) (1,-1)
[W ] [C ] [E ]  →  (-1, 0)  [C]  (1, 0)
[SW] [S ] [SE]     (-1, 1) (0, 1) (1, 1)
```

### 移动决策算法

1. **意图注册**: 每个代理评估8个邻域格子的吸引力
   - 吸引力 = 出口距离 - 拥挤惩罚 + 恐慌奖励

2. **决策策略**:
   - 80% 概率: 选择最优格子（贪心）
   - 20% 概率: 随机选择（探索）
   - 高恐慌(>0.6): 40% 随机

3. **冲突解决**: 多个代理目标同一格子时
   - 儿童(age<15): 优先级×1.5
   - 老年人(age>65): 优先级×1.3
   - 高恐慌: +0.5优先级
   - 随机打平局

4. **执行**: 只有赢家移动到目标格子

---

## Excel配置详解

### 基本布局 (前100行×100列)

```
行1-100, 列A-CV (对应坐标系统):
- 每个单元格代表网格中的一个格子
- 值0-7代表不同的单元格类型
- 条件格式自动着色（可选）
```

### 参数行 (102-110)

在列A输入参数值，列B为说明标签：

| 行 | 参数 | 默认值 | 说明 |
|----|------|--------|------|
| 102 | simulation_steps | 1000 | 最大模拟步数 |
| 103 | initial_population | 75 | 初始代理数 |
| 104 | panic_spread_rate | 0.05 | 恐慌传播速率 |
| 105 | panic_decay_rate | 0.01 | 恐慌衰减速率 |
| 106 | crowding_threshold | 5 | 拥挤阈值 |

### InitialState工作表 (可选)

手动指定初始代理位置：

| 列 | 说明 |
|----|------|
| A | AgentID (0, 1, 2, ...) |
| B | X坐标 (0-99) |
| C | Y坐标 (0-99) |
| D | 年龄 (5-80) |
| E | FamilyID |

---

## 输出文件说明

### ca_simulation_results.xlsx

多个工作表：

- **Config**: 输入的网格配置备份
- **AgentTrajectories**: 完整代理移动轨迹
  - 列: Timestep, AgentID, X, Y, PanicLevel, Evacuated, Age
- **Summary**: 统计汇总
  - 总时步数、疏散人数、疏散率、恐慌等级等

### ca_simulation_log.csv

详细的代理状态日志，每行一个记录：
```
timestep,agent_id,x,y,panic_level,evacuated,age,stamina,family_id
0,0,50,50,0.0,False,35,1.0,1
0,1,52,48,0.0,False,42,1.0,2
...
```

### ca_statistics.csv

每步的全局统计：
```
timestep,active_agents,evacuated_agents,avg_panic,max_panic,avg_stamina
0,75,0,0.0,0.0,1.0
1,75,0,0.001,0.01,0.999
...
```

### ca_heatmap.png

两个并排的热力图：
- 左: 拥挤密度（代理经过次数）
- 右: 恐慌等级（平均恐慌值）

---

## 高级用法

### 自定义代理属性

```python
from core.ca import CAAgent

# 创建特殊代理（例如安保）
agent = CAAgent(0, 50, 50, age=40, family_id=None)
agent.resilience = 0.95  # 高抗压性
agent.base_speed = 1.2   # 更快
```

### 自定义移动策略

编辑 `core/ca/ca_behaviors.py` 中的 `select_next_cell()` 函数：

```python
def select_next_cell(agent, environment, agents, grid):
    """自定义移动决策逻辑"""
    # 添加您的策略
    pass
```

### 集成到现有系统

CA系统完全独立，不影响原有的连续坐标系统：

```python
from main import main as run_continuous  # 原有系统
from main_ca import main as run_ca      # CA系统

# 运行任一系统
run_continuous()  # 或
run_ca()
```

---

## 性能预期

- **网格**: 100×100 = 10,000格子
- **代理**: 50-100个
- **时步**: 最多1,000步
- **复杂度**: O(N) 平均，O(N²) 最坏
- **运行时间**: <1秒（超快）
- **内存**: ~50MB（非常省）

---

## 验证和测试

### 基本测试

```bash
# 1. 网格初始化测试
python -c "from core.ca import CAGrid; g = CAGrid(100, 100); print('Grid OK')"

# 2. 代理创建测试
python -c "from core.ca import CAAgent; a = CAAgent(0, 50, 50); print('Agent OK')"

# 3. 完整演示
python test_ca_demo.py

# 4. Excel集成测试
python setup_ca.py
python main_ca.py
```

### 预期结果

演示运行应该：
- ✅ 成功放置75个代理
- ✅ 所有代理在1000步内疏散（通常<300步）
- ✅ 生成输出文件在 `output/` 目录
- ✅ 没有错误或警告

---

## 故障排除

### 问题: "ConfigFileNotFoundError"

**解决**: 运行 `python setup_ca.py` 创建模板

### 问题: "ImportError: No module named openpyxl"

**解决**: 安装 `pip install openpyxl`

### 问题: 代理不移动

**检查**:
- 确保环境中有出口
- 检查网格中是否所有地点都被标记为墙

### 问题: 疏散时间过长

**优化**:
- 增加出口数量
- 减少墙体障碍
- 调整 `GREEDY_PROBABILITY` 为更高值（`config/ca_settings.py`）

---

## 与现有系统的集成

### 共存模式

两套系统完全独立：
- **连续系统** (`main.py`): 社交力模型，连续坐标
- **离散系统** (`main_ca.py`): 元胞自动机，网格坐标

可同时运行两个系统进行对比分析。

### 数据共享

可在分析中共享某些数据：
```python
# 两个系统的日志都在 output/ 目录
# 可使用相同的热力图和统计工具
```

---

## 文件清单

| 文件 | 优先级 | 创建日期 | 用途 |
|------|--------|--------|------|
| `core/ca/ca_engine.py` | ⭐⭐⭐ | Phase 1 | 核心仿真 |
| `core/ca/ca_behaviors.py` | ⭐⭐⭐ | Phase 1 | 8邻域规则 |
| `io/excel_parser.py` | ⭐⭐ | Phase 2 | 读配置 |
| `io/excel_writer.py` | ⭐⭐ | Phase 2 | 写结果 |
| `analysis/ca_logger.py` | ⭐⭐ | Phase 3 | 日志记录 |
| `core/ca/ca_grid.py` | ⭐ | Phase 1 | 网格管理 |
| `core/ca/ca_agent.py` | ⭐ | Phase 1 | 代理类 |
| `core/ca/ca_environment.py` | ⭐ | Phase 1 | 环境管理 |
| `config/ca_settings.py` | ⭐ | Phase 3 | 配置 |
| `main_ca.py` | ⭐ | Phase 3 | 入口 |
| `test_ca_demo.py` | ⭐ | Phase 4 | 测试 |
| `setup_ca.py` | ⭐ | Phase 3 | 初始化 |

---

## 后续改进方向

- [ ] 火灾/烟雾动态模型
- [ ] 拥挤引发的踩踏事件
- [ ] 多出口智能分配
- [ ] 实时可视化（动画）
- [ ] GPU加速（NumPy/CuPy）
- [ ] 多场景参数扫描
- [ ] 机器学习优化疏散策略

---

## 许可和致谢

这是"Night at Museum"项目的扩展模块，实现了经典的元胞自动机模型。

作者：Claude Code
日期：2026年1月27日
版本：1.0-Beta

---

## 联系和支持

遇到问题？
1. 检查 `test_ca_demo.py` 是否正常运行
2. 查看 `output/` 目录中的日志
3. 审查 `config/ca_settings.py` 中的参数
