---
title: "1. 通过Lambda实现挂机评价"
chapter: false
weight: 20
tags:
  - advanced
---

## 实验目的

在这部分，您将学习如何将 AWS Lamda 和 Amazon DynamoDB 服务与您的Amazon Connect进行集成。

Amazon Connect 与其他 AWS 服务（如 AWS Lambda）的原生集成允许您为呼叫者创建动态、个性化的体验。

在本实验中，我们将借助AWS Lambda 和 Amazon DynamoDB服务，实现客服通话结束后邀请客户对本次服务进行评价。

本部分试验主要包含以下内容：

- 根据提供的示例创建 AWS Lambda 函数。
- 在Disconnect Flow中设计挂机评价流程。
- 通过在Disconnect Flow中集成Lambda将客户的评价写入DynamoDB。

本次实验使用到以下AWS服务：

* Amazon Connect
* Lambda
* DynamoDB