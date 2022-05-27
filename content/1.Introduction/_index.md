---
title: "Workshop整体介绍"
chapter: false
weight: 1
---

在这一系列实验中，我们将使用 Amazon Connect 服务构建基于云联络中心，并探索与其他 AWS 服务（如 AWS Lambda、Amazon DynamoDB和Amazon Lex 等）的集成，以构建现代且强大的联络中心。

本Workshop旨在介绍 Amazon Connect，帮助以前不了解Amazon Connect 的用户掌握搭建云联络中心的技能。

> 本实验涉及到的服务一部分可以免费使用， 但是也有多项服务可能会产生少量使用费用。请参阅定价页面以查看AWS Lambda、DynamoDB、Amazon Lex 和 Amazon Connect等服务的免费套餐情况和计费方式。

本次Workshop分为两部分：

- Amazon Connect基础：在这部分您可以了解以下技术内容：

1. 部署Amazon Connect实例。
2. 申请电话号码并设置Contact Flow。
3. 了解和编写Contact Flow。
4. 进行语音/聊天测试。
5. 查看实时/历史指标和报告。

- Amazon Connect进阶：从部分您可以了解以下技术内容：

1. 通过将Contact Flow与Lambda的集成实现挂机后评价，并将客户评价写入DynamoDB。
2. Amazon Connect与Lex集成实现智能客服。


{{% notice info %}}
一般来说，需要先完成基础部分，然后再进行进阶部分。
{{% /notice  %}}

如果您对基础部分比较熟悉，而打算直接做进阶部分的话，则须完成以下的基础部分（进阶部分会依赖以下内容）：
1. [创建Amazon Connect实例]({{< ref "Amazon Connect Basic/1.Deploy/1.DeployConnect.md" >}})
2. [申请电话号码]({{< ref "Amazon Connect Basic/1.Deploy/2.ClaimNumber.md" >}})
3. [编写联系流]({{< ref "Amazon Connect Basic/2.ContactFlow/4.WriteDemoContactFlow.md" >}})
