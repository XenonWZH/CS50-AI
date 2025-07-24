##  概率分布表示方法

对一个随机事件，概率分布可简化地用向量（vector）写成如下形式
$$\mathbf{P}(Flight) = \langle 0.6, 0.3, 0.1 \rangle$$

## 贝叶斯公式（Bayes' Rule）

$$P(b \mid a) = \frac{P(a \mid b)P(b)}{P(a)}$$

## 随机事件的条件概率

可以对随机事件定义条件概率。例如
$$\mathbf{P}(\text{C} \mid \text{rain}) = \frac{\mathbf{P}(\text{C}, \text{rain})}{P(\text{rain})} = \alpha \mathbf{P}(\text{C}, \text{rain}) = \alpha \langle 0.08, 0.02 \rangle = \langle 0.8, 0.2 \rangle$$
在此可将 $P(\text{rain})$ 看作常数，其值不重要（实际上可以倒推出来）。在已知联合概率时，其作用相当于常值 $\alpha$，使得作用后的概率分布的和为 $1$。

## 贝叶斯网络（Bayesian network）

贝叶斯网络满足下列条件：
- 为有向图
- 每个点均代表一个随机变量
- $X \to Y$ 代表 $X$ 为 $Y$ 的父亲
- 每个点 $X$ 代表一个随机变量，且均有概率分布 $P(X \mid Parents(X))$

## 推理（Inference）

$$\mathbf{P}(\text{X} \mid \mathbf{e}) = \alpha \mathbf{P}(\text{X}, \mathbf{e}) = \alpha \sum_{\mathbf{y}} \mathbf{P}(X, \mathbf{e}, \mathbf{y})$$
其中变量含义如下：
- $\text{X}$：待计算的随机变量
- $\mathbf{e}$：证据（evidence），表示已知道的事件
- $\mathbf{y}$：隐藏变量
- $\alpha$：归一化常数

于是可以考虑使用贝叶斯网络进行计算。

## 近似推理（Approximate Inference）

使用采样（Sampling）进行近似推理。实际上就是生成成千上万个随机样本以概率在贝叶斯网络中执行出结果，并进行结果统计。

该方法对于发生概率极小的事件估计效果不好。

## 似然加权法（Likehood Weighting）

与近似推理相似，有两点不同：
- 固定已知信息
- 生成样本时不考虑贝叶斯网络中的概率，但样本会被赋予实际发生概率的权重

## 隐马尔可夫模型（Hidden Markov Model）

在马尔可夫模型中加入可观测的数据。即给出原本马尔可夫模型后，再给出观测到的 $E_{t}$，且 $E_{t}$ 和需计算的状态 $X_{t}$ 有关。这也被称为传感器模型（Sensor Model）。

所有的马尔可夫模型都有假设：该状态仅取决于前一状态。

计算过程如下：
- 滤波（filtering）：根据从初始状态到当前的所有观测数据，计算当前状态的分布情况
- 预测（prediction）：根据从初始状态到当前的所有观测数据，对未来进行预测
- 平滑处理（smoothing）：根据从初始状态到当前的所有观测数据，推算某个历史状态的概率分布
- 最大似然解释（most likely explanation）：根据从初始状态到当前的所有观测数据，推算出最可能的状态序列