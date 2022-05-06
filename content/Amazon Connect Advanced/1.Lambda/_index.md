---
title: "1. 通过Lambda实现挂机评价"
chapter: false
weight: 20
tags:
  - advanced
---

## 实验目的
本实验在客服通话结束后邀请客户对本次服务进行评价，通过集成Lambda将客户的评价写入DynamoDB，最后使用Glue和Athena进行数据处理和查询。

本次实验使用到以下AWS服务：

* Amazon Connect
* Lambda
* DynamoDB
* Glue
* Athena