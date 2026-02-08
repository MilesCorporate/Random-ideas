每日工作整理 - 2025/09/15
主要针对了Nexus 3的清理需求编写了一套自动化工具，目前设计是通过Ansible在服务端部署cron job，定时拉取镜像名称然后上传到N3, 客户端拉下来然后进行合并去重然后对照筛选出没有在使用的镜像。

详细Repo地址：https://repo.advai.net/hengyi.li/automatedimageschecker

目前遇到的问题：
1. 有的跳板机没有办法上去 (aai-infra, atome-usw2) 所以无法看ansible是否可达
2. 有些机器无法通过跳板机连接
3. kubernetes的镜像现在还在想如何获得

每日工作整理 - 2025/09/16
1. 在郭老师的指导下购买了新的advanguard.ai域名的证书
2. 重新拉取了N3上所有的最新镜像
3. 在郭老师的指导下配置了advanguard.ai的域名并且根据需求文档301到https://advance.ai/advanguard-identity-verification/地址
4. 学习Kubernetes和nginx
5. 继续完善自动化获取目前正在使用的镜像的脚本，目前脚本支持docker, podman, ctr (containerd), nerdctl, crictl， 对于kubernetes方面还在探索如何自动化实现的方式
  1. 以及目前还在思考如何把自己的key跟着ansible一起带过去来自动拉repo (目前是手动拉了以后跑脚本获取到镜像列表并自动上传，这个部分还需要进一步的自动化）
  2. 和周老师讨论了一下我们认为直接用Docker去根据业务线筛top10最大的镜像，然后去问他们要不要可能是更好的解决方案
6. 在郭老师的指导下对AdvanceAI的Aliyun上的部分k8s主机进行停机并且删除

每日工作整理 - 2025/09/17
1. 继续N3清理的脚本的搭建，扩展到不只是Docker, 也扫描Maven和npm的repo看看这俩的大小
  1. 同时启动docker扫描的脚本，目前跑了一半了，最大的镜像就是guardian那边的，一个就10多个g, 有好几十个这样的
  2. Maven和NPM的脚本还在调试
    1. Maven的目前能把列表拉下来了，等跑完来整理，然后可以同样搞出top 10 最大的
    2. NPM也把列表拉下来了，总共4508个软件包，总大小4231.35mb，基本没啥清理的价值
  3. 之前的自动化的实现方案计划可以尝试用ansible来搞，我寻思一下怎么写
  4. 目前Maven, NPM, Docker都可以找出来最大的镜像了，可以探讨一下我们下一步的清理方案是怎样的
2. 结合目前业务配置学习Nginx (学习笔记在这）
  1. 同时去翻了MDN的文档，根据常见状态码(3xx, 4xx, 5xx类型）思考对应nginx上的策略


每日工作整理 - 2025/09/18
1. 完成了Nexus 3自动化脚本的编写
  1. 初步完成了Docker镜像的统计，目前对生产环境下正在使用的镜像和在Nexus 3上存在的镜像进行了交叉比对，详细的统计结果在这
    1. 目前拉取的生产环境在用的镜像包括AAI的Aliyun在新加坡和印尼的节点，AdvanceX的docker，BPS的阿里云在印尼的节点，在合并去重以后统计独立的镜像数量只有539个
    2. 目前对于大小方面的计算由于我们无法获取到每一个镜像所使用的原始镜像，只能获取到当前镜像的大小，所以目前只做了平均镜像大小来作为一个参考指标
  2. 完成了对NPM仓库的统计，由于占比非常小，结论是清理的效果不大，没有必要清理
  3. 对于Maven仓库的统计结果还需要进一步的校对和检查，但是目前来看总共占空间大小也只有9个G左右，所以影响不是很大，看后续是否有需求进行清理
2. 跟郭雨明老师学习了如何用elasticsearch api来删除索引
3. 跟周亮老师学习了APB业务线开机器并且分配公网IP的流程


每日工作整理 - 2025/09/22
1. 完成Nexus 3的镜像占用分析，完整分析报告在这
  1. 结论是Guardian的镜像是最主要占用空间的镜像，如果能进行清理，至少能够释放1TB的空间
  2. 所有未使用的镜像版本加起来总计可清理1.5TB的磁盘空间
2. 购买了ginee.com的证书，现在等待SSL2Buy方面进行验证
3. 跟随亮哥一起整理安全组
  1. 负责范围
    1. Atome-ID-MSI-Admin
    2. Atome-ID-Newco-Admin
    3. Atome AFI Data Admin
    4. Atome Paylater MY Admin
    5. Atome AFI Admin
    6. AtomeSG Admin (Aliyun Global)
  2. 目前只是先把这些安全组抓出来，看哪个安全组对应哪些规则，下一步计划对照亮哥之前整理出来的白名单对已经失效的ip进行标记
  3. 列表链接：Aliyun 安全组


每日工作整理 - 2025/09/23
1. 继续昨天的安全组清理工作，对比前缀列表IP与实际在用的IP, 标记出被弃用的
2. 跟进ginee.com的证书验证
3. 更新atomefin.com的证书并且提交工单
4. 在郭老师的指导下创建集群
  1. AdvanceX业务线在 AWS上的x-aws-sg-stg1集群


每日工作整理 - 2025/09/24
1. 完成AdvanceX的K8s集群配置
2. AdvanceX开新机器装了Sentry （8C32G)
  1. x-sentry.advai.net指向x-infra-sg-nginx-nlb 这个域名，然后x-infra-sg-nginx-nlb指向advancex-nginx-nlb-c30b2b3eecccac30.elb.ap-southeast-1.amazonaws.com. 这个lb
3. 继续ACL和安全组的整理
4. ginee.com证书进行后续配置并且更新上线
5. x-jenkins.advai.net指向x-infra-sg-nginx-nlb， 现在支持同时用adx-jenkins.advai.net访问和x-jenkins.advai.net访问，这么做主要目的是后期维护起来更加方便
  1. 和杜昕晓老师确认过，后面会建新的grafana和prometheus，所以目前的这两个域名就先不动，x-grafana.advai.net和x-prometheus.advai.net留给以后的新的grafana和prometheus
  2. 还需要和祁老师确认advancex-teleport.advai.net 能否指向x-teleport.advai.net 去
6. 和亮哥确认了以后对Atome-ID-Newco账号的前缀列表和访问控制的IP进行清理，并且添加现在使用的IP


每日工作整理 - 2025/09/25
1. 继续对ACL列表进行清理
2. 经过讨论以后，考虑到较大的影响范围，对于advancex-teleport.advai.net域名不进行更改为x-teleport.advai.net.
3. 响应kafka报警
4. 配置x-aws-sg-infra1的k8s集群装rancher，并且在rancher中加入stg集群
  1. 同时也配置了用户权限，现在杜昕晓老师也是admin了
  2. 注意rancher升级到2.9以后在以后的配置文件中需要多一行privateCA: true 的配置，要不然其它集群在加入时会出现找不到证书的错误
5. 整理之前的集群配置文档

每日工作整理 - 2025/09/26
1. 继续对ACL进行清理

每日工作整理 - 2025/09/28
1. 校对Aliyun安全组和ACL
2. 对AWS-SG-Global账号下的安全组和前缀列表进行整理
3. 排查atome id3-data-platform集群pod创建的时候出现的 cgroups报错问题
  1. 结论是cgroups v1的bug, 等待atome那边节后以后再看要不要升级


每日工作整理 - 2025/09/29
1. 完成AWS上的前缀列表整理，还需要进一步校对
2. 更新apaylater.com的证书
3. 和亮哥一起解决mp/flow-engine 在gitlab的存储库推送以后merge卡住的问题
  1. 结论是merge并不是卡住，而是一次性提交了太多的文件（数量多，文件大小也大）导致安全部门的ai扫描缓慢所以一直显示正在等待，建议分多次提交以后问题修复
4. 对ginee.com的SLB和CDN的证书应用更新
  1. 对于SLB的证书因为今天有来自生产那边的无法访问的反馈，为了谨慎起见，决定先用旧的证书保证生产，对于新的证书的替换需要进一步检查是否还存在其它影响
  2. 对于CDN那边的证书，我和亮哥商量后确认使用新的证书+Global Sign 的R3中间证书完成替换，并且与生产那边确认了替换以后之前的无法访问的问题得到解决


今天的事情总结一下觉的自己有时候不够冷静，就如同老大所说，回滚肯定是要做的，但是在做之前需要先知道为什么会出现这个问题，才能找到下次如何避免，不然只是治标不治本。

每日工作整理 - 2025/10/09
1. Genie双十开新机器，8C64G, prod-gemie-scale1， 按量付费，启动之前的scale3， 两台机器都会在双十以后预计会在12号停掉
  1. 处理scale1和scale3的部署问题
2. 继续进行AWS安全组的整理
3. Atome id2集群log使用情况统计
  1. 目前主要占空间的就是10.14.11.6 （log吃了32g），10.14.11.233，10.14.0.139（log吃了29g），10.14.0.138（log吃了23g），10.14.0.140（log吃了22g）
  2. 亮哥和业务那边对接了以后决定保留10天的，剩下的删掉
  3. 其它机器可能也存在这种问题，明天继续

每日工作整理 - 2025/10/10
1. id2, id3, my，stg6, stg5, stg4集群执行log清理
2. x的rancher将token过期时间改为永不过期
3. 排查gitlab token过期问题
  1. 根据Gitlab官方的文档显示，从2023年5月以后，Gitlab强制移除了永不过期的令牌（从16.0版本以后）
    1. 对于之前所有的设定了令牌永不过期的项目，Gitlab将会把令牌过期日期设为自从升级日期起的一年以后。我们当前使用的是Gitlab 16.11版本，所以在这个影响范围以内。
    2. 目前解决办法就是直接生成一个新的token就好（现在token时间最长1年，到期了以后就会在用户界面隐藏）
4. 给achatgpt-staging.advai.net配置nginx

每日工作整理 - 2025/10/11
1. 应ginee业务线需求释放scale1, 停止scale3
2. 整理需要更新的域名证书和域名
3. 整理aws上的集群log使用情况
  1. 扫描aws-infra-data-eks, jkt-prod-bmi-k8s, ph-prod-atome-k8s, sg-prod-atome-k8s, th-prod-atome-k8s, usw2-prod-atome-k8s集群
4. skywalking升配，4C32 -> 8C32


每日工作整理 - 2025/10/13
1. 响应业务线需求，对PH, MY的skywalking进行升配 (4C32G -> 8C32G)
2. 整理当前AWS和Aliyun集群上落到本地盘的log日志情况
3. 响应Atome OSS上有报告链接无法访问的问题
  1. 结论是开发那边用了错误的Key
  2. 顺便了解了现在我们的Key轮转机制
4. 更新advai.net的证书

每日工作整理 - 2025/10/14
1. advai.net完成证书配置，ginee.com更新正确的clb证书
2. advancegroup.com.cn, tagfactory.ai购买并配置证书
3. 172.28.64.148 机器扩容50G
4. 收集域名证书更新状况，文档链接域名更新列表
5. 给BPS的SFTP创建新的用户账户


每日工作整理 - 2025/10/15
1. 域名证书梳理，文档：域名证书到期时间对照表（2025-10-15更新）
2. 更新x-rancher的证书
3. vpn-bj和vpn-sg证书更新

每日工作整理 - 2025/10/16
1. 研究如何给logstash做HPA
  1. 数据源来自Kafka, 希望是根据延迟程度来进行扩缩
  2. 用了KEDA和Kubernetes自己的HPA的功能实现了根据Kafka源的日志堆积程度来动态对logstash集群的pod数量进行调整


每日工作整理 - 2025/11/10
1. 辅助Citrix证书更新
2. Genie开机器， 16 core 64G 内存型机器（按量付费），重新启用scale 3
3. sg-vpn 应用之前的证书更新
4. AWS Cloudfront可以创建免费的自动续签的证书，试验是否可以下载并且解密用于其他服务
  1. 关于费用问题需要和温文确认，但是上周五的回复是都免费的 ----> 或许以后DV证书可以用这个，省下不少
5.  整理每个业务线目前拥有的集群列表
6. 更新apaylater.net的证书
7. Atome rabbitmq-exporter加一个新的监听

每日工作整理 - 2025/11/11
1. 继续整理每个业务线目前拥有的集群列表
2. 继续之前的安全组整理
  1. 拆分表格，与现在的VPC, 办公室网络核对
3. Git LFS解决方案研究
  1. 来自业务需求: 有人往repo里面传大文件导致git merge卡住
  2. 虽然目前gitlab支持lfs，但是存储盘并没有挂出来，考虑到潜在的问题不建议使用lfs
  3. 最后的解决办法还是不要单次提交一大堆大文件
4. Atome 修正prometheus的一个监控指标
  1. sum by (rabbitmq_cluster) (rabbitmq_running{rabbitmq_cluster!="id-prod-message"}) < 2 而不是 sum by (clusters) (rabbitmq_running{clusters!="rabbit@prod-finance-mq2"}) < 2
  2. 应该是按照集群标签来而不是按照机器名字来

每日工作整理 - 2025/11/12
1. 调查凌晨集群pod集体重建的原因
  1. 目前调查到可能原因有
    1. gc内存吃满
    2. 探活失败
    3. etcd调度连不上 ---> 重启
2. Genie下线机器(prod-genie-scale1 释放，prod-genie-scale3停机）
3. Genie prod-genie-inventory4机器按量付费转包年包月
  1. 机器配置是8c16g
  2. 来自业务说的
  近期发现 inventory 的服务器CPU 相对紧张，导致了用户部分操作（WMS 打包过慢).
  增加一台inventory 服务器的目的是为了缓解用户打包慢的问题。

每日工作整理 - 2025/11/13
1. 探查sentry无法发告警的问题
  1. 最后发现是业务那边的dsn过期了导致的无法发送
2. 在kp机器上搭建squid代理服务器
  1. 主要配置项目

每日工作整理 - 2025/11/17
1. 研究周六出现的grafana机器卡死重启问题
  1. 目前查到是有一个opensearch的数据源在查找10.16.11.5这个机器，但是这个机器已经不存在了所以一直失败
2. genie.shop 域名配置nginx, 购买免费证书Zhen Li 李臻与Hengyi Li的会话 2025年11月17日
3. Atome grafana数据源存在情况整理
4. Bps sftp整理创建用户文档
5. umma.id 买证书

每日工作整理 - 2025/11/18
1. 继续探查周六Grafana机器死机的问题
  1. 怀疑和之前clickhouse机器崩溃是同源，目前查看了日志并没有发现异常
  2. 可能存在底层硬件问题
2. 辅助AAI的vault搭建

每日工作整理 - 2025/11/19
1. 做了一个生成签发请求和合并证书链的自动化脚本
2. 写vault搭建文档
3. Rabbitmq 升级准备
  1. 环境检查，插件兼容性检查
4. 辅助配置group op下的argocd

每日工作整理 - 2025/11/20
1. 完成group-op-k8s下的argocd配置ldap并且测试
2. 在kafka中新建一个topic，和log stash的配置，topic：Thirdparty_biz_log
3. opensearch 创建新的template - primary 为3，replica为1
  1. logstash-nginx_logs
  2. logstash-acenter-logs
  3. logstash-a_cloud_service_logs
4. 研究rabbitmq迁移准备工作
  1. 本地先起一个旧的一个新的，测试shovel脚本
  2. 测试federal插件
5. cdn.atome.ph cname回cloudflare

每日工作整理 - 2025/11/24
1. Atome修复rabbitmq自动清除7天未使用的队列的脚本
  1. 问题出在之前是两个字符串比较，应该改为两个整数比较，这样才能正确识别
2. 继续之前的RabbitMQ迁移准备工作

每日工作整理 - 2025/11/25
1. 开始准备Grafana Docker迁移工作
  1. 目前做好了镜像
  2. 在准备数据复制备份
  3. 打进了K8s正在测试
2. 辅助AAI Vault K8s的部署工作
3. Atome rancher 添加飞连白名单

每日工作整理 - 2025/11/26
1. 办公室白名单增加飞连IP - 全账号更新
2. Atome-sg arm节点池+2台，x86节点池-5台，stg4环境
3. atome msi账号开机器，配nginx和clb

每日工作整理 - 2025/11/27
1. 继续grafana k8s项目
2. AAI aai-ali-sg-sandbox1和sg-prod-advance-k8s接阿里云通知重启实例
3. Atome apps.atomecorp.net 配置dns解析和nginx

每日工作整理 - 2025/12/08
1. 继续Rabbitmq迁移准备工作
  1. stg环境从3.7.28升级到3.13.7
2. 创建ak （Tagolog服务，用aws transcribe服务）

每日工作整理 - 2025/12/09
1. rabbitmq测试集群升级从3.7 ---> 3.13
2. 开机器 - 刘凤宝需求 -
  1. groupsec-deepflow-kafka                16c32g, 1tb          c7i.4xlarge
  2. groupsec-deepflow-seconion          16c32g 500g       c7i.4xlarge
3. DNS解析
  t97.message.aixpay.co      CNAME       u57881698.wl199.sendgrid.net
  T97._domainkey.message.aixpay.co      CNAME      T97.domainkey.u57881698.wl199.sendgrid.net
  T972._domainkey.message.aixpay.co   CNAME     T972.domainkey.u57881698.wl199.sendgrid.net
  _dmarc.message.aixpay.co       TXT     v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@aixpay.co;
4. AtomeSG PH集群node pool 5台扩容到6台 （+1台）
5. atometh-prod-dba-dbbackup-awssga-advaidc-vm 机器关机（志刚需求，th迁移ob已完成，暂时不使用这个备份机器）

每日工作整理 - 2025/12/10
1. 继续测试集群物理机装的mq从3.7升级到3.13
  1. 形成升级文档 rabbitmq原地升级3.13.7
  2. 测试16.04版本安装和升级rabbitmq（带erlang升级）
2. 域名解析
  1. groupsec-onion.advai.net --->  10.13.5.136:443
  2. groupsec-kafka.advai.net:8080 ----> 10.13.7.77:8080

  每日工作整理 - 2025/12/11
1. Genie开机器，16C 64G 按量付费 - 双12大促
2. 测试rabbitmq换底层系统以后再升级的可行性
3. 排查sentry部分功能没有启用的问题
4.  groupsec-onion.advai.net 和 groupsec-kafka.advai.net 配置文件修复点退出登录出现了服务器地址的问题

每日工作整理 - 2025/12/15
1. kafka集群升级测试(2.8.2 升级到 3.9.1）
  1. 能直接roll上去，并且生成了文档 Kafka停机升级
2. freyr.atomecorp.net nginx添加一个新的location

每日工作整理 - 2025/12/16
1. 继续Kafka升级测试
2. 更新Atome SG infra集群标签
3. Genie 资源相关
  停用活动期间增加 的 服务器
  IP:
  172.28.128.45

  释放机器:
  IP:
  172.28.128.65
  172.28.128.64
  172.28.128.66
4. AAI -ali-sg-sandbox1 集群中一台ecs因阿里云底层硬件故障所以进行重启
5. 删除canal_apaylater_sg_apaylater_b topic （黄航）
6. 修正aixpay.co的txt解析 (shing)
7. x-prod-sentry01-awssga-advaidc-vm 机器磁盘扩容
8. aix项目开了两台机器安装新的rabbitmq （

每日工作整理 - 2025/12/17
1. AIX-rabbitmq完成配置
  1. 创建负载均衡和配置了集群，ha-mode
2. Genie排查wordpress机器磁盘堆满问题
  1. 结果是binlog导致的，协商以后决定关掉binlog
3. 给aix项目的doracloud创建新的安全组和前缀列表
4. 排查advanceX 访问bucket没权限的问题
5. aixpay.co 修正mx记录
6. 更新sftp白名单
7. X 印尼区域开通S3 Endpoint Gateway

每日工作整理 - 2025/12/18
1. genie协助排查之前的genie-prod-wp机器磁盘吃满问题
2. genie-prod-wp 上的mysql关掉binlog并且调整sync_binlog和innodb_flush_log_at_trx_commit参数为1
3. CBI 网络压测准备 CBI Tecno网络压测准备
4. genie开机器4c16g，包年包月prod-genie-shop1
5. ppd-id sftp-guardian-test 白名单添加
6. Advance x 印尼地区新建节点组，并且打了污点和标签

每日工作整理 - 2025/12/19
1. prod-bpsdata-jenkins机器释放
2. 测试kafka在容器的支持性
3. id3 tableau-cloud加白名单
4. 跟进101domain上关于.vn域名验证的问题

每日工作整理 - 2025/12/22
1. 继续kafka docker升级测试
  1. 目前卡在更新镜像以后容器起不来，遇到报错说无法与broker通信

每日工作整理 - 2025/12/23
1. 继续Kafka Docker升级测试
  1. 目前流程已经跑通，形成了文档 基于Docker的Kafka停机升级流程
2. Aix rabbitmq加监控
3. aix项目装kafka和zookeeper
4. prod-guardian-data 加日志轮转，目前设定值为3天，最大2g

每日工作整理 - 2025/12/24
1. 完成AIX的kafka和zookeeper的安装和配置
2. 继续测试docker升级kafka
3. id2的kafka磁盘扩容1T

每日工作整理 - 2025/12/25
1. 继续docker版本的zookeeper和kafka升级测试 Docker Kafka停机升级
2. 更新办公室白名单
3. stg5环境升级zookeeper和kafka

每日工作整理 - 2025/12/26
1. CBI Tecno网络压测
2. 准备STG6和STG4的Kafka和zookeeper升级
3. 前缀列表和安全组开始清理

每日工作整理 - 2025/12/29
1. terraform创建eks自动化项目 - stage1: 前期调查准备
2. aix的kafka打开日志记录（journald的）

每日工作整理 - 2025/12/30
1. 继续Terraform自动化工作
  1. 完成了eks的配置，还需要测试

每日工作整理 - 2026/1/4
1. 继续搭建Terraform构建框架
  1. 重构了整个目录结构以和aws调用相匹配
  2. 精简了每一个模块
2. AAI修复了bps和id集群node上ntp不同步问题
  1. timedatectl set-ntp true然后systemctl restart chronyd

每日工作整理 - 2026/1/5
1. 对于AAI 集群的节点NTP服务失去同步进行进一步排查
  1. 猜测可能是阿里云底层的物理机在频繁调整时间导致了chronyd
  2. 结论: chronyd切换源时间不及时，导致失去同步
    1. 目前设置的是minpoll 4 maxpoll 10， 所以切换源时间在几分钟到几个小时之间不等（取决于网络）
      1. 最小2^4秒 x 8次轮询, 最大2^10秒 x 8次轮询，网络卡了那重来
2. 继续Terraform自动化创建集群项目
  1. 目前已经完成了框架，需要调试和解决validate的时候的报错
3. 下线并删除myacard.biz, myacard.cn, 51qinmi.com域名解析
4. 添加白名单

每日工作整理 - 2026/1/6
1. AWS Terraform Workshop
2. 继续Terraform 构建EKS项目
  1. 现在等待找个平台测试
3. Atome办公室白名单整理更新
4. Aai stori添加白名单
5. Advancex 开机器，4c8g， turn服务器

每日工作整理 - 2026/1/7
1. Terraform EKS Workshop
2. AFI 办公室IP更新到白名单
3. 继续维修Terraform创建EKS的cluster模块，应该加上dependencies

每日工作整理 - 2026/1/8
1. Terraform创建EKS项目继续测试修改
2.  groupsec-onion.advai.net nginx配置修改后端端口为8443
3. 更新AFI Office和KP Office在白名单上的IP地址

每日工作整理 - 2026/1/9
1. Terraform脚本修订 - Aliyun
2. AAI 印尼阿里云创建一个新的 Elasticsearch - 用于迁移自建es的备份 -  4C32G * 6 - 1000GB

每日工作整理 - 2026/1/12
1. aai-ali-sg-sandbox1 集群上的 k8s 节点(10.27.2.60)因系统维护实例进行重启
2. Zookeeper kafka升级准备 （测试是否能不停机无感升级）
3. Atome PH环境 节后大升级项目准备

每日工作整理 - 2026/1/13
1. Kafka Zookeeper生产环境升级测试
  1. 发现旧版Kafka在zookeeper里的入口是 /kafka, 而新版kafka在zookeeper里的入口就变成了 /cluster.
    - 根据目前的测试结果，新旧集群都在线时，数据都还存在，能互通，但是cluster id更改了，可能是一个隐患
    - 在新zk加入集群以后，老zk都需要全部重启一遍
  2. 在ph的生产集群中，kafka的server.properties配置里有一行 /kafka， 这个是指定了zk的写入路径，所以在新的集群上的kafka也应该加上这个配置

每日工作整理 - 2026/1/14
1. mem.atomecorp.net配置nginx
2. 继续测试kafka和zookeeper生产环境升级流程并且搞了一个文档 Kafka & Zookeeper 生产环境升级手册
3. 更新nginx白名单 - 应用之前KP 和AFI Office发过来的最新的办公室IP
4. stg4机器扩盘 100g ---> 400g
5. th迁移资源整理 TH资源清单
6. groupsec-selefra-awssga 机器下掉绑定的sgr-public的安全组（来自凤宝）
7. group-infra-nexus-awssga-advaidc-vm 增加1T 磁盘

每日工作整理 - 2026/1/15
1. PH生产环境升级Zookeeper和Kafka准备 Kafka & Zookeeper 生产环境升级执行手册 PH环境Zookeeper & kafka升级

每日工作整理 - 2026/1/19
1. 调研Mirror Maker迁移方案
2. groupsec-asm-awssga-advaidc-vm  机器修复无法访问teleport的问题
3. Atome Infra MSK 添加Kafka堆积的报警
4. 统计新旧机器配置，为ph升级做准备 PH Zookeeper & Kafka 升级机器配置 PH Zookeeper & Kafka 机器当前配置

每日工作整理 - 2026/1/20
1. Ph kafka zookeeper升级项目最后一次测试
2. 改善MSK Grafana报警
3. PH kafka zookeeper 新机器加入了集群，开始了topic迁移

每日工作整理 - 2026/1/21
1. 继续ph环境topic迁移
2. 调查grafana报警时出现数据库锁的问题
3. 更新afi和kp办公室提供的ip到aws上
4. 统计ph环境操作系统版本
5. 新开机器 atome-prod-dbabackup02-awspha-advaidc-vm 4c16g 操作系统升级
6. rancher升级

每日工作整理 - 2026/1/22
1. 继续迁移kafka topic
2. 测试ph的Rabbitmq蓝绿部署升级的方案

每日工作整理 - 2026/1/26
1. ID2 Kafka Zookeeper升级准备配置文件
2. 继续测试Rabbitmq的升级方案 MQ 测试 TODO
3. aixpay.co添加TXT解析记录

每日工作整理 - 2026/1/27
1. PH 旧zookeeper和kafka下线
2. 校对id2的升级配置文件
3. 启动id2的升级计划，已经完成新集群的加入，开始迁移数据

每日工作整理 - 2026/1/28
1. 继续MQ生产环境升级方案的前期测试
2. 完成id2 topic迁移
3. aixpay.co添加txt记录

每日工作整理 - 2026/1/29
1. 继续rabbitmq测试
2. 修改gitlab runner的crontab，加入日志功能
3. aixpay.co 添加dmarc记录
4. atome排查eks auto scaling group计划外踢出机器的问题
5. grafana添加了一个新的dashboard用来监控节点污点的状态（看不可调度/不可达的节点有哪些）
  1. 并且加了一个报警
6. Ph zk5和6 磁盘扩容1t （现在这两台机器7t）
7. 开始准备MY 的Kafka ZK迁移

每日工作整理 - 2026/2/2
1. 开始准备MY集群的升级配置文件，准备开始迁移
2. 继续测试RabbitMQ升级
3. 探究Kafka 3.9升级后数据量看起来膨胀的问题
4. AAI添加SFTP空间


每日工作整理 - 2026/2/3
1. MY 集群升级Zookeeper Kafka
2. Atome MSI新建一个nginx机器和lb，配置路由
3. PH, ID2, MY zk kafka集群关掉apt的自动更新





OKR

2025 Q4 OKR

----
O1: 熟悉业务线，并逐步参与日常运维工作

KR1: 系统性学习业务线的架构，流程，和相关运维工具，并形成文档化笔记
KR2: 参与到五大业务线的日常运维工作中，即使响应临时发生的时间，并能够做出对应的操作
KR3: 熟悉并掌握支撑Genie, Atome, AdvanceX, Group, AAI 这五大业务线的核心工具和流程
KR4: 学习并掌握Kubernetes基础知识，能够理解其在公司业务中的应用场景，并能完成简单实操

-----

O2: 有效参与印尼的IDC重建工作

KR1: 做好在印尼的翻译工作，确保信息传递准确
KR2: 学习并理解数据中心的建设流程和方法，总结形成学习报告或复盘文档





2026 Q1 OKR

⸻

O1：完成 AWS 和 Aliyun 安全组与前缀列表的清理与优化

聚焦于存量治理，降低历史配置风险，提升云平台的可维护性与合规性。

KR1：完成 AWS 和 Aliyun 存量安全组规则梳理与清理，明确标识并删除无效、过期规则
KR2：完成前缀列表清理，删除冗余或不再使用的条目，并确保现有规则可追溯
KR3：沉淀安全组与前缀列表清理规范文档，形成可复用的定期复审流程

⸻

O2：保障集团日常云计算与中间件运维工作的稳定运行

通过及时响应与持续优化，确保日常运维对业务影响最小化。

KR1：保障 95% 以上的磁盘扩容类运维请求在 1 小时内完成处理
KR2：参与业务线问题排查与支持，80% 以上问题在约定时间内完成定位或解决
KR3：针对高频运维场景（服务部署、资源扩容等），推动流程优化或自动化改进，降低人工操作成本
⸻

O3：成功完成 AWS K8s 集群升级，并推进集群管理自动化

在保障稳定性的前提下，提升集群的可维护性与交付效率。

KR1：完成 AWS K8s 集群升级方案设计与执行，升级过程中无生产级事故
KR2：升级完成后，核心业务服务 在 2 小时内恢复正常运行，并完成基本功能验证
KR3：持续优化 Terraform 相关脚本与结构，支持集群的标准化创建与管理，减少手动操作依赖
