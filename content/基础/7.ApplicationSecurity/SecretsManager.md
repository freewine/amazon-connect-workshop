---
title: "使用 Secrets Manager 管理应用的用户名和密码"
chapter: false
weight: 73
tags:
  - beginner
---

## AWS Secrets Manager

AWS Secrets Manager 可帮助您保护访问应用程序、服务和 IT 资源所需的密钥。该服务使您能够轻松地管理和检索数据库凭证、API 密钥和其他密钥，并自动对密钥进行轮换。用户和应用程序通过调用 Secrets Manager API 来检索密钥，无需将密钥进行硬编码。Secrets Manager 通过适用于 Amazon RDS、Amazon Redshift 和 Amazon DocumentDB 的内置集成实现密钥轮换。此外，该服务还可以扩展到其他类型的密钥，包括 API 密钥和 OAuth 令牌。此外，Secrets Manager 使您能够使用精细权限来访问机密信息，并集中审核对 AWS 云、第三方服务和本地资源的密钥轮换。

本章节将介绍，如何使用 Secrets Manager 托管之前已部署的 Wordpress 数据库的密钥，并对密钥配置自动轮换，避免将数据库连接密钥以明文的方式保存在 Wordpress 配置文件中。

### 配置 Secrets Manager
1. 进入 Secrets Manager 控制台，创建新的密钥：
https://ap-northeast-1.console.aws.amazon.com/secretsmanager/home?region=ap-northeast-1#/newSecret?step=selectSecret

- 密钥类型：选择 ```RDS数据库的凭证```
- 用户名： Wordpress 数据库的用户名 ```wpadmin```
- 密码：  wordpress 数据库的密码 ```wpadmin123```
- 加密密钥： DefaultEncryptionKey
- 要托管的数据库： ```wordpress-cluster```

点击【下一步】按钮
![](/images/7.ApplicationSecurity/SecretsManager-1.png)
2. 在“密钥名称和描述”界面上，密钥名称输入: ```Wordpress-DB```。其他保留缺省值，点击【下一步】按钮。
3. 在“配置自动轮换”界面上：

- 自动轮换： 点击“启用自动轮换”单选框，默认30天自动轮换一次，可以设置为1-365天
- 轮换密钥的Lambda前缀： ```Wordpress-DB-Rotate```

最后点击【存储】按钮。

![](/images/7.ApplicationSecurity/SecretsManager-2.png)

{{% notice note %}}
如果启用密钥自动轮换，在密钥创建完成后，会自动进行一次轮换，修改当前密钥。
{{% /notice  %}}

由于 Wordpress 应用所在的 EC2 将要访问 Secrets Manager API 以获取 RDS 连接密钥，所以需要为 EC2 关联的 Instance Role 授权对密钥的访问。

在[使用Session Manager作为堡垒机方案]({{< ref "基础/5.SecOps/3.session_manager_operation.md" >}})中，
我们为WordpressServer1 / WordpressServer2 EC2实例设置过角色：SSM-Role，找到该角色，并拷贝该角色的ARN：
https://console.aws.amazon.com/iam/home?region=ap-northeast-1#/roles/SSM-Role

在 Secrets Manager 控制台，进入 Wordpress-DB 密码：
https://ap-northeast-1.console.aws.amazon.com/secretsmanager/home?region=ap-northeast-1#/secret?name=Wordpress-DB

修改**资源权限**，将 Principal 替换为上一步记录的角色 ARN
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "secretsmanager:GetSecretValue",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<SSM-Role的ARN>"
      },
      "Resource": "*"
    }
  ]
}
```
 ![](/images/7.ApplicationSecurity/SecretsManager-3.png)

### 修改 Wordpress 配置

1. 通过 Session Manager 登录 WordpressServer1， 使用 AWS CLI 测试获取 Secrets Manager 的密钥，此时数据库连接的密钥已经被轮换。
```
aws secretsmanager get-secret-value --secret-id Wordpress-DB --region ap-northeast-1
```
```
sh-4.2$ aws secretsmanager get-secret-value --secret-id Wordpress-DB --region ap-northeast-1
{
    "Name": "Wordpress-DB",
    "VersionId": "8e9cf16b-fc6f-40d0-bad2-969e1517afc8",
    "SecretString": "{\"username\": \"admin\", \"password\": \"7QqFAE[tpwx09Xz`;xh7noK8kHxL6~2{\", \"engine\": \"mysql\", \"host\": \"wordpress-cluster.cluster-cluqkc7jqkna.ap-northeast-1.rds.amazonaws.com\", \"port\": 3306, \"dbClusterIdentifier\": \"wordpress-cluster\"}",
    "VersionStages": [
        "AWSCURRENT",
        "AWSPENDING"
    ],
    "CreatedDate": 1611814554.139,
    "ARN": "arn:aws:secretsmanager:ap-northeast-1:699962710372:secret:Wordpress-DB-H01d56"
}
```
2. 通过 Composer 安装 PHP SDK 包。
```
cd /var/www/html
sudo yum install php-xml -y
sudo yum install php-mbstring -y
sudo php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
sudo php composer-setup.php
sudo php -d memory_limit=-1 composer.phar require aws/aws-sdk-php
sudo php -r "unlink('composer-setup.php');"
sudo chown apache:apache vendor
sudo chown apache:apache vendor/*
```
3. PHP SDK 安装完成后，编辑 Wordpress 配置文件 ```sudo vi /var/www/html/wp-config.php```，复制下面代码插入到第二行，在 "<?php"之后 
```
/** Get DB credentials from Secrets Manager */
require '/var/www/html/vendor/autoload.php';
use Aws\SecretsManager\SecretsManagerClient;
use Aws\Exception\AwsException;
$client = new SecretsManagerClient([
    'version' => '2017-10-17',
    'region' => 'ap-northeast-1',
]);
$secretName = 'Wordpress-DB';
$result = $client->getSecretValue([
    'SecretId' => $secretName,
]);
if (isset($result['SecretString'])) {
    $secret = $result['SecretString'];
} else {
    $secret = base64_decode($result['SecretBinary']);
}
$secrets = json_decode($secret,true);
$username = $secrets['username'];
$password = $secrets['password'];
$dbhost = $secrets['host'];
```
并修改 ```/var/www/html/wp-config.php```中连接数据库的配置，用 Secrets Manager 的变量替换明文配置。

```
/** MySQL database username */
define( 'DB_USER', $username );     

/** MySQL database password */
define( 'DB_PASSWORD', $password );

/** MySQL hostname */
define( 'DB_HOST', $dbhost );
```
4. 修改完成后，保存文件，然后重新启动 HTTP 服务。
```
sudo service httpd restart
```

**使用 Session Manager 登录到 WordpressServer2 中，重复一遍上述步骤：**
 - 安装 PHP SDK
 - 修改 Wordpress 配置文件```/var/www/html/wp-config.php```
 - 重启 HTTP 服务。

### 验证 Secrets Manager

在浏览器中打开之前部署的 CloudFront URL，验证 Wordpress 是否能正常连接数据库。
```CloudFrontURL/wp-login.php```，默认用户名：wpadmin，默认密码：wpadmin123
![](/images/7.ApplicationSecurity/SecretsManager-4.png)

### 轮换 Secrets Manager 中托管的密钥

打开 Secrets Manager 控制台，进入 Wordpress-DB 密钥，点击 “立即轮换密钥”。
![](/images/7.ApplicationSecurity/SecretsManager-5.png)

在 WordpressServer 上，再次通过 AWS CLI 验证密钥轮换成功。
```
aws secretsmanager get-secret-value --secret-id Wordpress-DB --region ap-northeast-1
```
```
sh-4.2$ aws secretsmanager get-secret-value --secret-id Wordpress-DB --region ap-northeast-1
{
    "Name": "Wordpress-DB",
    "VersionId": "84062102-6932-420a-9af8-b5041f049b0e",
    "SecretString": "{\"username\": \"admin\", \"password\": \"1fy#^Qg&J*`5;_IfrnokvV15$5I4V~Sl\", \"engine\": \"mysql\", \"host\": \"wordpress-cluster.cluster-cluqkc7jqkna.ap-northeast-1.rds.amazonaws.com\", \"port\": 3306, \"dbClusterIdentifier\": \"wordpress-cluster\"}",
    "VersionStages": [
        "AWSCURRENT",
        "AWSPENDING"
    ],
    "CreatedDate": 1611841892.01,
    "ARN": "arn:aws:secretsmanager:ap-northeast-1:699962710372:secret:Wordpress-DB-H01d56"
}
```
在浏览器中打开之前部署的 CloudFront URL，验证 Wordpress 是否能正常连接数据库。
```CloudFrontURL>/wp-login.php```，默认用户名：wpadmin，默认密码：wpadmin123
 ![](/images/7.ApplicationSecurity/SecretsManager-4.png)


