# WebUi自动化测试平台
 
## 概述

    目的：
        通过该平台实现WebUi自动化测试的相关工作，例如：项目的管理；服务器Hub的管理；测试用例的管理（包括：创建、编辑、删除等）；自动化测试执行与管理、自动化测试报告的管理以及生成供持续集成的CI/CD的测试用例；    
    核心框架：
        1）使用python+selenium+pytest+allure来实现底层框架的封装；
        2）再通过Python Django+mysql来实现Web前后端不分离的开发方式来实现的，以及数据持久化与管理工作。

## 特性

- 功能模块介绍：
- - 用户及权限管理：实现用户创建及权限的管理工作；
- - 测试项目的管理：实现项目的创建、编辑、删除等工作；
- - 服务器Hub的管理：实现了服务器HUB的配置及管理工作；
- - 测试用例的管理：实现用例的新建、编辑、删除等管理工作；
- - 自动化测试执行与管理：实现了测试用例的执行工作，以及测试用例的导出供CI/CD持续集成测试提供的操作入口；
- - 自动化测试报告的管理：实现测试报告的自动保存与管理工作；

- 框架或组件的功能介绍：
- - Django框架负责：服务器后端处理逻辑与为前端提供HTTP请求与响应服务、以及提供启动自动化测试插件、测试结果/报告等数据保存到MYSQL数据库等功能；
- - Django Admin管理后台负责：前端页面UI的展示、用户登录、用户登出与相关测试用例、测试报告或管理数据的录入与保存、用户权限的管理与设置等功能；
- - Selenium/Appium/Request框架测试插件负责：自动化测试的底层服务及实现自动化测试工；例如：操作事件封装、数据驱动、元素定位、页面的跳转、frame的切换等；
- -	PYTEST框架负责：测试用例的共享前置/后置、测试用例的参数化、测试用例的skip和xfail处理、测试结果的断言、插件机制扩展等功能；
- -	MYSQL负责：用户注册、用户权限设置、测试用例、测试报告等数据的存储等功能；
- -	Allure框架负责：测试数据的收集与测试报告的生成等功能。

- 基于自动化测试管理平台在Linux部署
- - 项目所需依赖：请见requirements.txt文件;
- -	在Linux上安装python环境；
- - 在Linux上安装MySql环境；
- -	安装python虚拟环境：virtualenvwrapper，并创建虚拟环境；
- -	安装PyTest插件工具；
- -	复制Django项目打包到Linux系统；
- -	在虚拟环境中运行Django项目即可；
- -	Nginx负载均衡服务器配置与启动运行

- 使用说明：运行项目时一定要先启动服务器端以及配置服务器端口等;
- 贡献指南：若程序报错，可以通过日志文件来查找对应的错误;
- 许可证: 该项目放在github上，可供任何人员使用，即不需要任何许可证;
- 版本历史: 当前最新版本为：V1.0.0.0;
- 致谢: 感谢所有为该项目做出贡献的人员：无。
- 作者：陈强
- 联系方式: 49983655@qq.com

## 平台需要创建的数据表
### 1、项目管理表字段及创建sql脚本：
    - 项目名称、项目负责人、项目描述、创建时间
    - CREATE TABLE `webuiautotest_product` (`id` bigint(20) NOT NULL AUTO_INCREMENT,`itemName` varchar(100) NOT NULL,`itemDesc` varchar(200) DEFAULT NULL,`itemManager` varchar(30) DEFAULT NULL, `createTime` datetime(6) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;SET FOREIGN_KEY_CHECKS=1;
    
### 2、服务器HUB管理表字段及创建sql脚本：
    - 服务器名称、服务器地址、创建时间
    - CREATE TABLE `webuiautotest_seleniumhubserver` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `serverName` varchar(100) NOT NULL,`serverType` varchar(20) NOT NULL,`serverAddress` varchar(200) DEFAULT NULL,`serverPort` int(11) DEFAULT NULL,`createTime` datetime(6) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;SET FOREIGN_KEY_CHECKS=1;

### 3、用例管理表字段及创建sql脚本：
    - 用例编号、用例名称（主键）、前置条件（外键索引）、浏览器类型（外键索引）、后置条件（外键索引）、执行结果、执行时间、所属项目（外键索引）
    - CREATE TABLE `webuiautotest_webcase` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `caseName` varchar(100) NOT NULL, `browser` varchar(50) NOT NULL,`FrontPostManager_id` bigint(20) DEFAULT NULL, `Product_id` bigint(20) NOT NULL, `SeleniumHubServer_id` bigint(20) NOT NULL, `created_time` datetime(6) NOT NULL, `headless` varchar(20) NOT NULL,PRIMARY KEY (`id`), KEY `WebUiAtuoTest_webcas_FrontPostManager_id_631681cb_fk_WebUiAtuo` (`FrontPostManager_id`), KEY `WebUiAtuoTest_webcas_Product_id_d6b90e52_fk_WebUiAtuo` (`Product_id`), KEY `WebUiAtuoTest_webcas_SeleniumHubServer_id_d2f2492d_fk_WebUiAtuo` (`SeleniumHubServer_id`), CONSTRAINT `WebUiAtuoTest_webcas_FrontPostManager_id_631681cb_fk_WebUiAtuo` FOREIGN KEY (`FrontPostManager_id`) REFERENCES `webuiautotest_frontpostmanager` (`id`), CONSTRAINT `WebUiAtuoTest_webcas_Product_id_d6b90e52_fk_WebUiAtuo` FOREIGN KEY (`Product_id`) REFERENCES `webuiautotest_product` (`id`), CONSTRAINT `WebUiAtuoTest_webcas_SeleniumHubServer_id_d2f2492d_fk_WebUiAtuo` FOREIGN KEY (`SeleniumHubServer_id`) REFERENCES `webuiautotest_seleniumhubserver` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;SET FOREIGN_KEY_CHECKS=1;

    
    - 将：用例执行步骤单独成表字段及创建sql脚本：
    - 用例名称（外键）、步骤顺序、操作关键字、元素名称、操作数据、操作描述
    - sql:略；
    
    - 将：前置条件、后置条件单独成表字段及创建sql脚本：
    - 前/后置名称（主键）、描述
    - sql:略；
    
    - 将：前/后置条件要执行步骤单独成表字段及创建sql脚本：
    - 用例名称（外键）、步骤顺序、操作关键字、元素名称、操作数据、操作描述
    - sql:略；
    
### 4、测试报告管理表字段及创建sql脚本：
    - 测试报告标题、测试日期、报告类型、报告详情等
    - CREATE TABLE `simpleui_app_testreport` (  `id` bigint(20) NOT NULL AUTO_INCREMENT, `title` varchar(1024) NOT NULL, `report_type` varchar(200) DEFAULT NULL, `desc` varchar(1024) NOT NULL,  `report_detail` varchar(1024) NOT NULL,  `created_time` datetime(6) NOT NULL,  PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=349 DEFAULT CHARSET=utf8; SET FOREIGN_KEY_CHECKS=1;
    
    
    
