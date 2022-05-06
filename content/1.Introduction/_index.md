---
title: "Workshop整体介绍"
chapter: false
weight: 1
---

在这一系列实验中，我们将使用 Amazon Connect 服务构建基于云的联络中心，并探索与其他 AWS 服务（如 Amazon DynamoDB、Amazon Lex 和 AWS Lambda）的集成，以构建现代且强大的联络中心。

本Workshop旨在介绍 Amazon Connect，旨在帮助以前不了解 AWS 或 Amazon Connect 的用户。

 本实验涉及到的服务部分可以免费使用， 但是也有多项服务可能会产生一些使用费用。 请参阅定价页面以查看AWS Lambda、DynamoDB、Amazon Lex 和 Amazon Connect 中使用的服务的免费套餐使用情况和成本。

本次Workshop分为两部分：

- Amazon Connect基础：这部分从技术上来说，您可以了解以下技术内容：

1. 部署Amazon Connect实例
2. 申请电话号码并设置Contact Flow
3. 了解和编写Contact Flow
4. 进行Voice/Chat测试
5. 查看日志、统计数据和报告


{{% notice info %}}
请先完成基础部分的实验。
{{% /notice  %}}

- Amazon Connect进阶：这部分从技术上来说，您可以了解以下技术内容：

1. 通过Contact Flow的设计以及Lambda的集成实现挂机后评价
2. Amazon Connect与Lex集成实现智能客服


{{% notice info %}}
这部分需要在完成基础内容以后进行操作。
{{% /notice  %}}

如果您对基础部分都比较熟悉，而打算直接做进阶部分的话，则必须完成以下的基础部分（进阶部分会依赖以下的部分）：
1. [申请电话号码]({{< ref "Amazon Connect Basic/1.Deploy/2.ClaimNumber.md" >}})
2. [编写联系流]({{< ref "Amazon Connect Basic/2.ContactFlow/4.WriteDemoContactFlow.md" >}})







