---
title: "2.3 部署Connect Chat UI"
chapter: false
weight: 23
tags:
  - advanced
---

## 实验目的

> 前置条件
>* 该部分依赖步骤2.2中，部署完成的Amazon Connect实例以及导入的Contact Flow和配置完成的Amazon Lex。如果上述步骤未完成，建议先完成步骤2.2。

该部分实验使用Amazon Chat UI与客户端进行集成，该部分中分为两个模块：

* 模块一：Chat UI集成
* 模块二：CCP集成后台

![](/images/chatbot/asynccustomerchatux.png?width=1000px)

本次实验使用到以下AWS服务：

* Amazon Connect
* Amazon Lex
* CloudFormation
* API Gateway
* CloudFront
* S3
* Lambda
* DynamoDB