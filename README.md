# Amazon Connect介绍

Amazon Connect 是一个易于使用的全渠道云联络中心，可帮助公司以更低的成本提供卓越的客户服务。 十多年前，亚马逊的零售业务需要一个联络中心为我们的客户提供个性化、动态和自然的体验。我们找不到满足我们需求的产品，所以我们构建了Amazon Connect。构建完成之后，我们对所有企业开放了此服务。如今，成千上万的公司使用 Amazon Connect服务，每天为数百万客户提供服务，客座席数量从 10 到数万不等。

Amazon Connect 从一开始就设计支持全渠道，为您的客户和代理提供跨语音和聊天的无缝体验。Amazon Connect还提供基于技能的路由、强大的实时和历史分析，以及易于使用的管理工具——所有这些都采用即用即付的定价策略。所有这些，意味着 Amazon Connect 简化了联络中心的运营，提高代理效率，降低成本。您可以在几分钟内建立一个可以扩展以支持数百万客户的联络中心。

# Workshop介绍
在这一系列实验中，我们将使用 Amazon Connect 构建基于的云联络中心，并探索与其他 AWS 服务（如 AWS Lambda、Amazon DynamoDB和Amazon Lex 等）的集成，以构建现代且强大的联络中心。

本Workshop旨在介绍 Amazon Connect，帮助以前不了解Amazon Connect 的用户掌握搭建云联络中心的技能。
本Workshop分为两部分：

## Amazon Connect基础
这部分介绍Amazon Connect的基本功能，内容包括：
1. 部署Amazon Connect实例。
2. 申请电话号码并设置Contact Flow。
3. 了解和编写Contact Flow。
4. 进行语音/聊天测试。
5. 查看实时/历史指标和报告。

## Amazon Connect进阶
这部分介绍Amazon Connect的高级用法，内容包括：
1. 通过将Contact Flow与Lambda的集成实现挂机后评价，并将客户评价写入DynamoDB。
2. Amazon Connect与Lex集成实现智能客服。

> 一般来说，需要先完成基础部分，然后再进行进阶部分。
>
> 如果您对基础部分比较熟悉，而打算直接做进阶部分的话，则必须完成以下的基础部分（进阶部分会依赖以下内容）：
>
> 1. [创建Amazon Connect实例]({{< ref "Amazon Connect Basic/1.Deploy/1.DeployConnect.md" >}})
> 2. [申请电话号码]({{< ref "Amazon Connect Basic/1.Deploy/2.ClaimNumber.md" >}})
> 3. [编写联系流]({{< ref "Amazon Connect Basic/2.ContactFlow/4.WriteDemoContactFlow.md" >}})
