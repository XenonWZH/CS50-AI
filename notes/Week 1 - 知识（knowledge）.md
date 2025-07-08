## 逻辑运算

### 与或非

没啥可讲的。

### 蕴含（implication）

| $P$ | $Q$ | $P \implies Q$ |
| --- | --- | -------------- |
| T   | F   | T              |
| F   | T   | T              |
| T   | F   | F              |
| T   | T   | T              |

### 双条件（biconditional）

| $P$ | $Q$ | $P \iff Q$ |
| --- | --- | ---------- |
| F   | F   | T          |
| F   | T   | F          |
| T   | F   | F          |
| T   | T   | T          |

## 结构

- 模型（model）：模型会对每个命题符号（propositional symbol）赋予真值（truth value）（T / F）
- 知识库（knowledge base）：确认为真的命题集合
- 推理（inference）：从既有命题推导出新命题的过程

### 逻辑蕴含关系（entailment）

$\alpha \models \beta$：$\alpha$ 蕴含 $\beta$，其中 $\alpha, \beta$ 为命题，即当 $\alpha$ 为真，$\beta$ 必为真。

## 模型检验算法（Model Checking）

实际上就是穷举法。

若需检验知识库 $\operatorname{KB}$ 是否有 $\operatorname{KB} \models \alpha$
- 枚举所有可能的模型
- 若对每个 $\operatorname{KB}$ 为真的模型，$\alpha$ 均为真，则 $\operatorname{KB} \models \alpha$
- 否则，有 $\operatorname{KB} \not\models \alpha$

## 推理规则（Inference Rules）

实际上就是简单逻辑

- $((\alpha \implies \beta) \wedge \alpha) \models \beta$
- $(\alpha \wedge \beta) \models \beta$
- $(\neg(\neg\alpha)) \models \alpha$
- $(\alpha \implies \beta) \models ((\neg\alpha) \vee \beta)$
- $(\alpha \iff \beta) \models ((\alpha \implies \beta) \wedge (\beta \implies \alpha))$
- $(\neg(\alpha \wedge \beta)) \models ((\neg\alpha) \vee (\neg\beta))$
- $(\neg(\alpha \vee \beta)) \models ((\neg\alpha) \wedge (\neg\beta))$
- $(\alpha \wedge (\beta \vee \gamma)) \models ((\alpha \wedge \beta) \vee (\alpha \wedge \gamma))$
- $(\alpha \vee (\beta \wedge \gamma)) \models ((\alpha \vee \beta) \wedge (\alpha \vee \gamma))$

利用此可对命题进行建图进行搜索
- 初始状态：最开始的知识库
- 行动：推理规则
- 转移模型：推理规则作用后的知识库
- 目标测试：查看待证命题是否存在于知识库
- 路径代价函数：所需推理规则数量或证明步骤数

## 归结法（resolution）

显然有如下规则
- $$\left( \left( P \vee \left( \bigvee_{i = 1}^{n} Q_{i} \right) \right) \wedge (\neg P) \right) \models \bigvee_{i = 1}^{n} Q_{i}$$
- $$\left( \left( P \vee \left( \bigvee_{i = 1}^{n} Q_{i} \right) \right) \wedge \left( (\neg P) \vee \left( \bigvee_{i = 1}^{n} R_{i} \right) \right) \right) \models \left( \bigvee_{i = 1}^{n} Q_{i} \right) \vee \left( \bigvee_{i = 1}^{n} R_{i} \right)$$

有以下概念
- 子句（clause）：析取句（disjunction，即通过“或”连接）中的文字（iterals，命题符号或其否定）
- 合取范式（conjunctive normal form）：以子句合取（conjunction，即通过“且”连接）的命题

于是遵循以下规则，所有命题均可转化为合取范式的形式，即 CNF

| 原命题                                 | 转化命题                                                     |
| ----------------------------------- | -------------------------------------------------------- |
| $\alpha \iff \beta$                 | $(\alpha \implies \beta) \wedge (\beta \implies \alpha)$ |
| $\alpha \implies \beta$             | $(\neg\alpha) \vee \beta$                                |
| $\neg(\alpha \wedge \beta)$         | $(\neg\alpha) \vee (\neg\beta)$                          |
| $\neg(\alpha \vee \beta)$           | $(\neg\alpha) \wedge (\neg\beta)$                        |
| $\alpha \vee (\beta \wedge \gamma)$ | $(\alpha \vee \beta) \wedge (\alpha \vee \gamma)$        |

## 通过归结规则的推理（Inference by Resolution）

有归结法

| 子句 1              | 子句 2                     | 归结后的子句              |
| ----------------- | ------------------------ | ------------------- |
| $P \vee Q$        | $(\neg P) \vee R$        | $(Q \vee R)$        |
| $P \vee Q \vee S$ | $(\neg P) \vee R \vee S$ | $(Q \vee R \vee S)$ |
| $P$               | $\neg P$                 | $()$（空子句，恒为假）       |


若需检验知识库 $\operatorname{KB}$ 是否有 $\operatorname{KB} \models \alpha$
- 检查 $(\operatorname{KB} \wedge (\neg \alpha))$ 是否为矛盾
    - 若为矛盾，则 $\operatorname{KB} \models \alpha$
    - 否则，无逻辑关联

即有过程

若需检验知识库 $\operatorname{KB}$ 是否有 $\operatorname{KB} \models \alpha$
- 转化 $(\operatorname{KB} \wedge (\neg \alpha))$ 为 CNF
- 持续查看是否可用归结法生成新的子句
    - 若成成空子句，则产生矛盾，有 $\operatorname{KB} \models \alpha$
    - 若无法生成空子句，则 $\operatorname{KB} \not\models \alpha$

## 一阶逻辑（First-Order Logic）

有概念
- 常量符号（Constant Symbol）
- 谓词符号（Predicate Symbol）
谓词符号可作为常量的属性 $\operatorname{Predicate}(\operatorname{Constant})$ 判断真假，可进行逻辑运算 $\neg\operatorname{Predicate}(\operatorname{Constant})$，谓词符号也可表示二元关系 $\operatorname{Predicate}(\operatorname{Constant}_{1}, \operatorname{Constant}_{2})$。

## 量词

就是 $\forall$ 和 $\exists$，没可啥讲的。