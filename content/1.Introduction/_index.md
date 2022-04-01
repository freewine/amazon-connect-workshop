---
title: "整体实验介绍"
chapter: false
weight: 1
---

{{% notice note %}}
如果你已经对整个实验有所了解，则可以跳过当前部分，而进入下一个步骤。否则，建议请阅读本部分，了解整个实验的目的以及所需要进行的步骤。
{{% /notice  %}}

通过本次安全实践动手训练营，您可以了解如何把在AWS平台上实现全方位的安全实战。
本次训练营分为两部分：

- 基础：这部分从技术上来说，您可以了解以下技术内容：

1. 安全事件监控
2. 网络监控
3. 数据保护
4. 系统运维的安全
5. 数据库的安全审计
6. 应用系统的安全

{{% notice info %}}
请先完成基础部分的实验。
{{% /notice  %}}

- 进阶：这部分从技术上来说，您可以了解以下技术内容：

1. 配置Security hub
2. 使用Detective分析数据
3. CloudTrail日志实时监控
4. CloudFront日志实时监控
5. 配置WAF保护ALB
6. WAF日志实时监控
7. WAF自动化
8. 数据库审计日志实时监控以及归档到S3
9. 使用Privatelink对外暴露应用系统
10. 使用SageMaker IP Insights算法实现基于机器学习的异常IP检测

{{% notice info %}}
这部分需要在完成基础内容以后进行操作。
{{% /notice  %}}

如果您对基础部分都比较熟悉，而打算直接做进阶部分的话，则必须完成以下的基础部分（进阶部分会依赖以下的部分）：
1. [启用CloudTrail]({{< ref "基础/2.OperationMonitor/1.EnableCloudTrail.md" >}})
2. [部署云端基础架构]({{< ref "基础/3.networksecurity/7.vpc_basic.md" >}})
3. [对数据库启用审计日志]({{< ref "基础/6.databaseaudit/4.rds_audit_log.md" >}})
