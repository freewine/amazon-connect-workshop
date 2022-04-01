---
title: "RDS安全进阶"
chapter: false
weight: 63
tags:
- advanced
---

本节将介绍以下内容

* [为RDS启用SSL](#rds_mysql_ssl)
* [使用IAM用户登录RDS](#rds_mysql_iam)

## 为RDS启用SSL{#rds_mysql_ssl}
您可以使用安全套接字层(SSL)来加密MySQL数据库实例的连接。

在RDS数据库实例创建时，SSL证书被安装在数据库实例上。SSL证书会将数据库实例终端节点作为SSL证书的公用名(CN)包含在内，以防止欺诈攻击。

### 下载RDS证书
适用于AWS RDS的根证书:
* 适用于Global所有区域的在[这里](https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem)
* 适用于Global个别区域的证书，可以参考[这个页面](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)
* 适用于中国北京区域的在[这里](https://s3.cn-north-1.amazonaws.com.cn/rds-downloads/rds-cn-ca-2019-root.pem)
* 适用于中国宁夏区域的在[这里](https://s3.cn-north-1.amazonaws.com.cn/rds-downloads/rds-cn-ca-2017-cn-northwest-1-root.pem)

### 通过命令行使用SSL连接
```bash
# 建立SSL连接并验证服务器端CA
mysql -h rdsid.xxxxxx.rds-ap-northeast-1.amazonaws.com --ssl-ca=./rds-ca-2019-root.pem \
-u admin -p -d test
```

```sql
-- 连接上以后通过SQL语句查询所有连接的状态
MySQL [test]> SELECT id, user, host, connection_type
    ->        FROM performance_schema.threads pst
    ->        INNER JOIN information_schema.processlist isp
    ->        ON pst.processlist_id = isp.id;
+-------+--------------+---------------------+-----------------+
| id    | user         | host                | connection_type |
+-------+--------------+---------------------+-----------------+
| 12820 | rdsrepladmin | 10.7.2.254:42276    | TCP/IP          |
| 13546 | admin        | 172.27.22.111:39816 | SSL/TLS         |
|  5308 | rdsadmin     | localhost:39178     | TCP/IP          |
+-------+--------------+---------------------+-----------------+
3 rows in set (0.01 sec)
```
可以看到admin用户的连接是通过SSL/TLS保护的。

### 限制用户必须用SSL连接
```sql
-- mysql >=5.7
ALTER USER 'your_user'@'%' REQUIRE SSL;

-- mysql <=5.6
GRANT USAGE ON *.* TO 'your_user'@'%' REQUIRE SSL;
```

### 使用SSL连接RDS的Java示例
请参考[这个页面](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/ssl-certificate-rotation-mysql.html)

## 使用IAM用户登录RDS{#rds_mysql_iam}
您可以使用IAM数据库身份验证对您的数据库实例进行身份验证。利用此方法，您在连接到数据库实例时将无需使用密码，而是使用身份验证令牌。生成的身份验证令牌将在**15分钟**后失效。

IAM数据库身份验证具有以下特点和限制：
* 数据库的出站和进站网络流量是使用SSL/TLS加密的。
* 您可以使用IAM集中管理对数据库资源的访问，而不是单独管理对每个数据库实例的访问。
* 数据库实例每秒的最大连接数可能会受到限制，建议200连接/秒以下才使用。
* IAM数据库身份验证不支持IAM策略里面的全局条件上下文，比如不能限制用户来源于某个IP地址段。
* IAM数据库身份验证不支持RDS实例的CNAME。
* 可以将IAM数据库身份验证用作个人临时访问的授权机制。只在需要的时候生成令牌，临时授权个人来连接RDS。

### 启用IAM数据库身份验证
默认情况下，IAM数据库身份验证是禁用的。可以通过以下步骤启用：
1. 选择要修改的数据库实例，点击**修改**按钮。
2. 在数据库身份验证部分中，选择**密码和IAM数据库身份验证**以启用IAM数据库身份验证。
![启用IAM数据库身份验证](/images/6.DatabaseAudit/rds_security_adv_1.png)
3. 点击**继续**按钮。
4. 在修改计划部分中选择**立即修改**，点击**修改数据库实例**按钮。
![立即应用](/images/6.DatabaseAudit/rds_security_adv_2.png)
这个修改不会造成RDS重启。

### 使用IAM身份验证创建数据库账户
MySQL身份验证是由AWSAuthenticationPlugin处理的，这是AWS提供的一个插件，可以与IAM无缝协作以验证您的IAM用户的身份。
```sql
-- 创建DB用户iamreadonly
CREATE USER iamreadonly IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'; 
-- 赋予select权限
GRANT SELECT on *.* to 'iamreadonly'@'%';
```
在使用AWSAuthenticationPlugin创建一个账户后，可以像管理其他数据库账户一样管理此账户。

这里创建了一个只有select权限的RDS用户iamreadonly，用来临时授权给人使用。

### 适用于IAM数据库访问的IAM策略
IAM策略里面，Resource ARN的内容是下面的格式。

arn:aws:rds-db:[region]:[account-id]:dbuser:[DbId]/[db-user-name]

[DbId]或[db-user-name]可以用*来匹配所有RDS实例或所有db用户。

比如，对东京区域的账户123456789012，允许IAM User以iamreadonly的身份去连接RDS实例db-ABCDEFGHIJKL01234，需要下面这条策略。

```json
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Effect": "Allow",
         "Action": [
             "rds-db:connect"
         ],
         "Resource": [
             "arn:aws:rds-db:ap-northeast-1:123456789012:dbuser:db-ABCDEFGHIJKL01234/iamreadonly"
         ]
      }
   ]
}
```
### 将IAM策略附加到IAM用户或角色
在创建允许数据库身份验证的IAM策略之后，需要将该策略附加到IAM用户或角色。
1. 在IAM控制台的导航窗格中，选择**策略**。
2. 点击**创建策略**按钮。
3. 修改上面的JSON文档，粘贴到JSON策略编辑器里面。这个策略允许在所有RDS数据库使用iamreadonly用户。
![IAM策略](/images/6.DatabaseAudit/rds_security_adv_3.png)
4. 给策略起个名称**rds_iam_auth_iamreadonly**，点击**创建策略**按钮。
![创建策略](/images/6.DatabaseAudit/rds_security_adv_4.png)
5. 选中并点击刚才创建的**rds_iam_auth_iamreadonly**策略，在**策略用法**标签页，点击**附加**按钮
![选中策略](/images/6.DatabaseAudit/rds_security_adv_5.png)
6. 选中用户test，把策略附加到这个IAM用户，点击**附加策略**按钮。

   这里利用到的test用户是一个没有控制台登陆权限也没有任何IAM策略的**编程访问**用户。后续生成令牌的操作，将依据这里附加的IAM策略利用test用户的AK/SK来执行。
![附加策略](/images/6.DatabaseAudit/rds_security_adv_6.png)

### 通过命令行使用IAM身份验证连接到RDS MySQL

awscli安装可以参考[安装说明](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/install-cliv2-linux.html)，配置可以参考[配置说明](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)。配置时使用test用户的Access Key/Secret Key。

首先管理员用awscli命令行工具生成IAM身份验证令牌。
```bash
RDSHOST="rdsmysql.123456789012.ap-northeast-1.rds.amazonaws.com"
TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --region ap-northeast-1 --username iamreadonly)"
# 在终端上显示令牌，管理员复制并发送给申请连接RDS的申请人
echo $TOKEN
```
令牌是几百个字符的URL形式的字符串，申请人拿到令牌以后就可以连接RDS了。
```bash
RDSHOST="rdsmysql.123456789012.ap-northeast-1.rds.amazonaws.com"
# 这里申请人用得到的令牌给TOKEN赋值，令牌只有15分钟有效期
TOKEN="rdsmysql.123456789012.ap-northeast-1.rds.amazonaws.com:3306/?Action=connect&DBUser=iamreadonly&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=900&X-Amz-Date=yyyymmdd..."

mysql --host=$RDSHOST --ssl-ca=./rds-ca-2019-root.pem --enable-cleartext-plugin --user=iamreadonly --password=$TOKEN
```
注意：mariadb的client不支持--enable-cleartext-plugin参数，必须使用mysql的client。

如果想安装mysql client，可以参考下面的命令：
```bash
# 安装mysql5.7 client
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client
```

