# 目标：最大化$N$天内的消耗量

## model 1

**最大化目标函数**：
maximize $\sum_{i=1}^{N} x_i$

**约束条件**：

1.  每一天的消耗量的计算公式：

    $$
    x_i = \sum_{j=1}^{M} t_{ij} c_{j}, \forall i
    $$

2.  每一天的总运动时间不超过 MaxDayTime：

    $$
     \sum_{j=1}^M t_{ij} \le MaxDayTime, \forall i
    $$

3.  每一天单项运动的时间不超过 MaxSingleDayTime：

    $$
     t_{ij} \le MaxSingleDayTime：, \forall i, j
    $$

4.  休息：运动 MinCont 天至少要休息 1 天：

    > if 运动了 MinCont 天 then 休息 1 天
    > i.e., 任意连续 MinCont 天的运动时间之和不超过 MinCont 天

    $$
    \sum_{k=i}^{i+MinCont} y_k \le MinCont, \\ \forall i \le N-MinCont
    $$

5.  休息：针对运动类型，每种运动相邻两次至少要间隔 MinInterval 天：

    > if 第$i$天和第$j$天运动了 then 第$i$天和第$j$天之间至少有 MinInterval 天休息或做其他运动  
    > i.e., if 第$i$天进行了第$j$种运动 then 第$i+1$天至第$i+MinInterval$天不能进行这种运动

    $$
    \sum_{k=i}^{i+MinInterval} z_{kj} \le 1, \forall j, i \le N-MinInterval
    $$

6.  每天运动种类数不超过 EN：

    $$
    \sum_{j=1}^M z_{ij} \le EN, \forall i
    $$

7.  $x_i$和$y_i$的取值关系：

    $ y_i = 1 \iff x_i > 0, \forall i $

    $ y_i = 0 \iff x_i = 0, \forall i $

    等价于

    $y_i * BigM \ge x_i, \forall i$

    $y_i \le x_i, \forall i$ (可以省略)

8.  $z_{ij}$和$t_{ij}$的取值关系：

    $z_{ij} = 1 \iff t_{ij} > 0, \forall i, j$

    $z_{ij} = 0 \iff t_{ij} = 0, \forall i, j$

    等价于

    $z_{ij} * BigM \ge t_{ij}, \forall i, j$

    $z_{ij} \le t_{ij}, \forall i, j$ (可以省略)

**优化1**：
让BigM尽可能小

---

**变量定义**：

$x_i$：第$i$天的消耗量

$y_i$: 第$i$天是否运动

$t_{ij}$: 第$i$天的第$j$种运动的时间

$z_{ij}$: 第$i$天的第$j$种运动是否做了

**参数定义**：

$N$：天数

$M$：运动种类数

$c_{j}$: 第$j$种运动的单位时间（10min）消耗能量



## model 2

在 model 1 的基础上，调整 y 变量的表达，去掉BigM

**约束条件**：
1. 约束1-6、8 保持不变

2. $y_i$的取值关系（约束7）修改如下：

   $$
   y_i = \max_{j} z_{ij}, \forall i
   $$

   等价于

   $$
   y_i \ge z_{ij}, \forall i, j \\
   $$

## model 3

在 model 2 的基础上，
添加对称性消除约束


**约束条件**：
model 2 的约束条件保持不变，添加如下约束：
1> 为了最大化能量消耗，第一天肯定要运动
$$
   y_1 = 1
$$

2> 消耗能量最大的运动，是最“划算”的（假设为j*），所以不妨第一天就做,
$$
   z_{1,j*} = 1
$$


<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config"> MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });</script>
