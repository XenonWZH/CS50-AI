## 搜索（search）的结构

- 初始状态（initial state）
- 行动（action）
- 转移模型（transition model）
- 目标测试（goal test）
- 路径代价函数（path cost function）

## 节点（node）

节点是一种记录以下信息的数据结构：
- 状态（a state）
- 父节点（a parent）
- 行动（an action）
- 路径成本（a path cost）

实际上相当于 OI 中对抽象状态的建图过程。

## 搜索过程

- 从一个只包含初始状态（initial state）的边界（frontier）开始
- 从一个空的已探索集合（explored set）开始
- 重复以下步骤
    - 如果边界为空，则无解（no solution）
    - 移除边界中的一个点（node）
    - 如果这个点能通过目标测试（goal test），返回这个解（solution）
    - 将该节点加入已探索集合
    - 拓展该节点（expand node），将可达的未在已探索集合或边界中的节点加入边界

实际上与 OI 中的搜索过程逻辑一样。

## 搜索算法

### DFS & BFS

和 OI 中图论的 DFS & BFS 一致。

### 无信息搜索（uninformed search）/ 启发式搜索（informed search）

- 无信息搜索：不使用任何特定问题的知识（problem-specific knowledge）的搜索
    - eg：DFS & BFS
- 启发式搜索：使用特定问题的知识以更快找到解的搜索
    - eg：GBFS

### 贪心最佳优先搜索（greedy best-first search, GBFS）

一种搜索算法，其拓展节点时总是选择距目标最近的节点（使用启发式函数（heruristic function）$h(n)$ 计算）。

### A* 搜索（A* Search）

一种搜索算法，其拓展节点时选择 $g(n) + h(n)$ 的值最小的节点
- $g(n)$ 表示到达当前节点所需的代价
- $h(n)$ 表示预估从当前节点到达目标所需的代价

可以证明 A* 搜索在以下条件下可选出最优解
- $h(n)$ 具备可采纳性（admissible）（永不高估真实代价）
- $h(n)$ 具备一致性（consistent）（对于任意节点 $n$ 和通过代价 $c$ 到达的后继节点 $n'$，总有 $h(n) \leq h(n') + c$）

A* 通常需要大量内存。

### 极小化极大算法（Minimax）

在双人对抗游戏中，将一方赢记为分数 $1$，将另一方赢记为 $-1$，将平局记为 $0$。则有下列情况
- $\operatorname{MAX}$（先手）想要分数最大化
- $\operatorname{MIN}$（后手）想要分数最小化

于是对于游戏，有下列结构
- $S_{0}$：初始状态
- $\operatorname{PLAYER}(s)$：返回状态 $s$ 应当该哪个玩家进行操作
- $\operatorname{ACTIONS}(s)$：返回对于状态 $s$ 的合法的操作
- $\operatorname{RESULT}(s, a)$：返回对状态 $s$ 执行操作 $a$ 之后的状态
- $\operatorname{TERMINAL}(s)$：判断状态 $s$ 是否为终局状态
- $\operatorname{UTILITY}(s)$：返回终局状态 $s$ 的数值

于是对于一个状态 $s$，有以下操作
- $\operatorname{MAX}$ 玩家将对任意的 $a \in \operatorname{ACTIONS}(s)$，计算并选取 $\operatorname{MIN-VALUE}(\operatorname{RESULT}(s, a))$ 的最大值
- $\operatorname{MIN}$ 玩家将对任意的 $a \in \operatorname{ACTIONS}(s)$，计算并选取 $\operatorname{MAX-VALUE}(\operatorname{RESULT}(s, a))$ 的最小值

对于 $\operatorname{MAX-VALUE}(state)$ 函数，有如下算法
```python
def MAX_VALUE(state):
    if TERMINAL(state):
        return UTILITY(state)
    v = -math.inf
    for action in ACTIONS(state):
        v = max(v, MIN_VALUE(RESULT(state, action)))
    return v
```
$\operatorname{MIN-VALUE}(state)$ 函数同理。

### Alpha-Beta 剪枝（Alpha-Beta Pruning）

对于 Minimax 中的 $\operatorname{MAX-VALUE}(state)$ 函数，考虑剪枝。对于该函数，记录 $v$，则在计算 $\operatorname{MIN-VALUE}(\operatorname{RESULT}(state, action))$ 时，若遍历到的值小于 $v$，则该枝无法被选中，无需计算。

~~实际上从时间复杂度的角度来看这种优化基本没用（？）~~

### 深度受限极小化极大算法（Depth-Limited Minimax）

一般问题使用 Minimax 体量巨大，无法计算，考虑使用深度受限的 Minimax 即可。
对于到达最大深度的状态 $s$，考虑使用估计函数（evaluation function）来估计在当前状态下游戏的预期效用。