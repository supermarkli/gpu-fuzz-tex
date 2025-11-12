![image-20251107151619542](assets/image-20251107151619542.png)![image-20251107151640474](assets/image-20251107151640474.png)

![image-20251107165241875](assets/image-20251107165241875.png)

![image-20251107151659243](assets/image-20251107151659243.png)

**GPUVerify: A Verifier for GPU Kernels (GPUVerify：一个GPU内核验证器)** 这篇论文介绍了一种名为 **GPUVerify** 的静态验证工具，专门用于自动证明用OpenCL或CUDA编写的GPU内核程序中不存在**数据竞争 (data races)** 和**屏障发散 (barrier divergence)** 这两类并发Bugs 。该工具的核心创新是提出了一种新颖的“同步、延迟可见性” (SDV) 形式化操作语义 ，它不仅精确定义了GPU特有的屏障发散问题，还允许将对复杂并发内核的分析**简化为对一个等效的\*顺序\*程序的分析** 。这种简化完全避免了对线程交错的显式推理 ，并允许工具自动推导验证所需的循环不变量 。GPUVerify 在163个真实内核上的评估表明，它能够高效且自动地验证大量现实世界中的GPU程序 。

![image-20251107151726495](assets/image-20251107151726495.png)

**Detection and Correction of Silent Data Corruption for Large-Scale High-Performance Computing (面向大规模高性能计算的静默数据损坏检测与纠正)** 这篇论文针对HPC（高性能计算）系统中由硬件引起的、无法被ECC等常规手段检测到的**静默数据损坏 (SDC)** 问题，提出了一种基于**进程冗余**的**检测和纠正**方案 。作者开发了 **RedMPI**，这是一个透明的MPI库，它通过创建应用进程的**双重或三重“副本”** ，并假设SDC最终会体现在MPI消息的差异上 。RedMPI在消息接收端对来自不同副本的消息（或其哈希值）执行**在线投票算法**，从而能即时识别并纠正损坏的数据，保证程序继续正确运行 。实验证明，若不加防护，单个SDC会迅速“级联”污染整个系统 ，而RedMPI能以0-30%的适度开销成功纠正数千条错误消息，甚至发现了测试集群上未知的真实硬件故障 。

![image-20251107151748845](assets/image-20251107151748845.png)

**NNSMITH: Generating Diverse and Valid Test Cases for Deep Learning Compilers (NNSMITH：为深度学习编译器生成多样化且有效的测试用例)** 这篇论文提出了一种名为 **NNSmith** 的模糊测试工具，旨在为TVM、TensorRT等深度学习（DL）编译器发现Bugs 。NNSmith通过两大核心技术解决了DL编译器Fuzzing的挑战：首先，它利用轻量级的算子规范和SMT求解器来**生成语法和语义均\*有效\*（valid）且结构多样的DNN模型**，确保测试用例能被编译器接受并深入测试其转换逻辑 ；其次，它采用**基于梯度的搜索**来寻找模型输入和权重，以**避免在执行过程中产生浮点异常值（NaN/Inf）**，从而防止Bugs被掩盖或产生误报 。通过将编译后模型的输出与参考后端（如PyTorch）进行差分测试 ，NNSmith成功在多个主流编译器中发现了**72个新Bugs**，并实现了比现有工具高32.7倍的唯一分支覆盖率 。

![image-20251107144941317](assets/image-20251107144941317.png)

**Compiler fuzzing through deep learning** 这篇论文提出了一种名为 DeepSmith 的革新性编译器Fuzzing方法，它**使用深度学习模型（LSTM）** **来自动学习如何生成测试程序**，而不是依赖传统Fuzzer（如CSmith）所需的手动编写的复杂语法 。DeepSmith 在大型真实代码库（如GitHub上的OpenCL内核）上进行训练 ，并学会了生成在语法和结构上看起来很真实的程序 ，然后通过差分测试找出Bugs 。该方法开发成本极低（500行代码，12小时训练），生成的**测试用例平均只有20行**（远小于CLSmith的1189行），并且能发现包括CLSmith无法发现的Bugs在内的**67个Bugs** 。

![image-20251107145124109](assets/image-20251107145124109.png)

**Fuzzing Deep Learning Compilers with HirGen** 这篇论文介绍了一种名为 HIRGEN 的Fuzzer，它专门用于测试深度学习（DL）编译器（如TVM）中**最容易出错的高级中间表示（High-Level IR）优化阶段** 。HIRGEN 使用**覆盖率引导**策略来生成多样化的计算图 ，并在转换为IR时利用**函数封装**等语言特性来测试复杂的优化 ；它还提供“破坏性”模式来故意生成无效IR以测试异常处理 。该工具使用三种测试预言机：崩溃、跨硬件（CPU/GPU）的差分测试，以及对比优化前后IR的变异测试 。HIRGEN 成功在 TVM 中发现了**21个Bugs**，其中14个被确认与高级IR优化阶段相关 。

![image-20251107151859132](assets/image-20251107151859132.png)

**History-Driven Fuzzing For Deep Learning Libraries** 这篇论文介绍了一款名为 Orion 的新型模糊测试工具，它通过分析**历史漏洞数据**来指导对 TensorFlow 和 PyTorch 库的测试 。研究者首先对376个历史漏洞进行实证研究 ，并基于其根本原因构建了一套**Fuzzing启发式规则** 。Orion 使用这些规则来**指导性地生成**已知的、容易触发问题的输入组合（如张量形状不匹配），以及**生成角例输入**（如极大/极负值、空值）。与传统Fuzzer不同，Orion还扩展了测试范围，覆盖了文档不全但很关键的内部“开发者API” 。Orion 共报告了135个漏洞，其中69个是未知的，并且在性能上超越了现有的Fuzzer 。

![image-20251107145355500](assets/image-20251107145355500.png)

**A Comprehensive Study of Deep Learning Compiler Bugs** 这篇论文是对深度学习（DL）编译器Bugs的一次系统性实证研究 。研究人员从 TVM、Glow 和 nGraph 三个主流DL编译器中收集并手动分析了 603 个Bugs ，从根本原因、症状和发生阶段三个维度进行了分类 。研究发现，**类型问题**（特别是张量类型）是最常见的根本原因 ，**崩溃 (Crash)** 是最常见的症状 ，而**高级和低级IR（中间表示）转换阶段**是Bugs最集中的地方 。基于这些发现，论文提供了未来DL编译器测试的指导方针，并开发了一个名为 TVMfuzz 的原型工具，成功发现了8个新Bugs 

![image-20251107145437338](assets/image-20251107145437338.png)

**Deep Learning Library Testing via Effective Model Generation** 这篇论文提出了一种名为 LEMON 的新型深度学习（DL）库测试方法，旨在解决测试模型不足和Bugs难以暴露的问题 。LEMON 通过**模型变异**（包括层级和层内变异）来自动生成新的DL模型作为测试输入 。其核心创新是采用一种**启发式引导策略**，优先选择那些能够“放大” (Amplify) 不同DL库（如TensorFlow、Theano）之间输出差异的变异模型，从而使Bugs更容易被检测到 。通过使用差分测试作为预言机 ，LEMON 在4个主流库的最新版本中成功检测到**24个新Bugs** ，并证明其生成的模型能显著放大Bugs效应，平均提升率达27%至357% 。

![image-20251107145638699](assets/image-20251107145638699.png)

**KLEE: Unassisted and Automatic Generation of High-Coverage Tests for Complex Systems Programs (KLEE：为复杂系统程序全自动生成高覆盖率测试)** 这篇论文介绍了一款强大的**符号执行工具 KLEE**，它能自动为复杂的、与环境交互密切的系统程序（如GNU COREUTILS）生成达到极高代码覆盖率的测试用例 。KLEE通过在LLVM字节码上执行程序，将输入视为*符号值*，从而探索多条执行路径 ；当路径终止或发现错误时，它通过约束求解器生成一个能触发该路径的具体测试用例 。KLEE通过高效的约束求解优化（如反例缓存）和对文件系统、系统调用等“环境”的精确建模 ，在89个COREUTILS工具上实现了平均超90%的行覆盖率，显著超越了开发者耗时15年构建的手动测试套件 ，并总共发现了56个严重Bugs（包括COREUTILS中潜藏15年的Bugs） 。

![image-20251107154738317](assets/image-20251107154738317.png)



![image-20251107155451170](assets/image-20251107155451170.png)

**An Integrated GPU Power and Performance Model (一个集成的GPU功耗和性能模型)** 这篇论文提出了一个**集成的GPU功耗与性能（IPP）预测模型**，旨在找到最优的活动处理器（核心）数量以最大化能源效率 。作者指出，对于受内存带宽限制的应用，启用所有GPU核心并不能提升性能，反而会浪费电力 。IPP模型创新地结合了一个分析性的计时模型来预测执行时间，从而*在没有硬件性能计数器或架构模拟器的情况下*推算出动态功耗 ，并且该模型还考虑了温度上升对功耗的影响 。实验证明，通过使用IPP模型预测的最佳核心数，在受内存带宽限制的基准测试中，GPU的运行时能耗平均可节省10.99% 。（这篇是为了说明内存复杂，容易出错）

![image-20251107155604673](assets/image-20251107155604673.png)

 **iGUARD: In-GPU Advanced Race Detection (iGUARD：GPU内的先进竞争检测)** 这篇论文介绍了一款名为 **iGUARD** 的运行时软件工具，用于检测现代GPU程序中因错误使用**高级同步功能**（如作用域同步、独立线程调度ITS和协作组CG）而导致的**数据竞争** 。与以往依赖CPU分析导致性能低下的工具不同 ，iGUARD 创新地**在GPU上\*执行\*所有竞争检测逻辑** ，利用GPU自身的并行性将检测速度提高了15倍 。它使用NVIDIA的NVBit二进制插桩工具 来监控内存和同步操作，应用“happens-before”和“lockset”算法 ，因此**无需重新编译源代码** 。iGUARD 成功在21个GPU程序中检测到**57个新的数据竞争**，且无误报，其中包括NVIDIA官方库中的Bugs 。

![image-20251107160133324](assets/image-20251107160133324.png)

**An Automated End-to-End Optimizing Compiler for Deep Learning (TVM：一个端到端的深度学习自动优化编译器)** 这篇论文介绍了 **TVM**，一个**端到端的深度学习优化编译器** ，旨在解决将DL模型高效部署到多样化硬件（如移动CPU、GPU、FPGA）的难题 。TVM不依赖于厂商手写的算子库（如cuDNN） ，而是通过两个层级的优化来自动生成高性能代码：首先，它在图层面执行算子融合（Operator Fusion）等优化 ；其次，它利用一个基于机器学习的代价模型（ML-based Cost Model） ，在一个巨大的调度（Schedule）搜索空间中，自动探索并*预测*出针对特定硬件的最佳底层代码实现 。实验表明，TVM生成的代码在服务器GPU、移动CPU和GPU等多个平台上的性能均达到甚至超越了（1.2x至3.8x）最先进的手动优化库 。

![image-20251107160345244](assets/image-20251107160345244.png)

![image-20251107160609599](assets/image-20251107160609599.png)

**Silent Data Corruptions: Microarchitectural Perspectives (静默数据损坏：微架构视角)** 这篇论文对**静默数据损坏（SDC）** 这一日益严重的问题进行了深入的**跨层微架构分析**，旨在揭示硬件故障是如何传播并最终导致程序输出错误的。鉴于大型数据中心（如Meta、Google）的报告显示SDC发生率高于预期 ，且传统的ECC和软件冗余方法存在开销大、覆盖不全的局限性 ，作者通过对一个现代乱序处理器（模拟Arm Cortex-A72）的**11个关键硬件结构**（如缓存、寄存器堆、TLB等）进行故障注入模拟 ，系统地量化了不同硬件单元对SDC的“贡献率”。研究发现，**L1数据缓存**（53.4%）和**L2缓存**（36.9%）的数据区是导致SDC的**最脆弱**部分 ，而像ROB、LQ和SQ等深层流水线结构中的故障几乎总会导致可检测的**崩溃**，因此产生SDC的概率接近于零 。一个关键见解是，虽然大多数SDC由“数据损坏”引起 ，但仍有相当一部分（超10%）是由“执行时间错误”或“指令流改变”等**非数据错误**导致的 ，这些错误可能**无法被传统的软件冗余方法检测到** 。此外，研究还发现，尽管**操作系统内核指令**占比极低（<10%），但它们在L1和L2缓存中引发的SDC占比却高达**30%以上** 。

![image-20251107160710411](assets/image-20251107160710411.png)

**U-Net: Convolutional Networks for Biomedical Image Segmentation (U-Net：用于生物医学图像分割的卷积网络)** 这篇论文提出了一种名为 **U-Net** 的卷积神经网络架构，专门用于解决**生物医学图像分割**任务，特别是解决了该领域**训练样本极少**的难题 。U-Net的“U形”架构由一个捕获上下文的**收缩路径**（ contracting path）和一个实现精确定位的对称**扩张路径**（expansive path）组成 。其核心创新在于**跳跃连接（skip connections）**，它将收缩路径中的高分辨率特征图与扩张路径中上采样后的特征图相**拼接（concatenation）** ，从而使网络能够在进行精确像素定位的同时结合深层的上下文信息 。通过结合大量的**数据增强**（尤其是弹性形变 ）和一种**加权损失**（weighted loss）来分离接触的细胞 ，U-Net能够从极少的图像中进行端到端训练 ，并在ISBI 2015细胞跟踪挑战赛中以巨大优势获胜 。

![image-20251107161928881](assets/image-20251107161928881.png)

**PointPillars: Fast Encoders for Object Detection from Point Clouds (PointPillars：用于点云对象检测的快速编码器)** 这篇论文提出了一种名为 **PointPillars** 的新型神经网络架构，用于处理自动驾驶等场景中的LiDAR**点云3D对象检测** 。为了解决现有方法要么慢（如VoxelNet ）要么不准（如固定编码器 ）的困境，PointPillars创新地将点云**划分为垂直的“柱子”（Pillars）** 。它首先使用一个PointNet网络来学习每个Pillar内点云的特征 ，然后将这些学到的特征“散布”回一个2D**伪图像（pseudo-image）** 。这个伪图像随后可以被高效的2D卷积网络（如SSD ）直接处理，从而**完全避免了昂贵的3D卷积** 。PointPillars在保持极高精度的同时，在KITTI基准上达到了**62 Hz**（乃至105 Hz）的极快检测速度，大幅超越了当时所有的SOTA方法 。

![image-20251107173312255](assets/image-20251107173312255.png)

Guardian: Safe GPU Sharing in Multi-Tenant Environments (Guardian：多租户环境中的安全GPU共享) 这篇论文提出了 Guardian，一个为解决云环境中因多租户空间共享（spatial-sharing）GPU而导致的内存安全问题而设计的软件系统 。现有的解决方案（如NVIDIA MIG）依赖于导致利用率低下的静态分区 ，或者（如NVIDIA MPS）缺乏故障隔离能力，即一个租户的非法内存访问会使所有共同运行的应用崩溃 。Guardian通过一种PTX级（虚拟汇编）插桩技术 来提供内存隔离，它首先将GPU内存划分为独立的、连续的逻辑分区 ，然后通过在每个内核的加载和存储指令前插入轻量级的边界检查指令（两个按位操作） ，强制使任何越界访问“环绕”回其自己的分区内 。这种方法透明地支持PyTorch等使用闭源库的框架 ，与（不安全的）MPS相比仅慢4.84%，但与（安全的）时间共享相比，总执行时间提高了37% 

![image-20251107165014460](assets/image-20251107165014460.png)

![image-20251107165102878](assets/image-20251107165102878.png)

![image-20251107165137505](assets/image-20251107165137505.png)

