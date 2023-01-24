import csv
import math
import re


def main():
    # input()
    data = read_file('vacancies_with_skills.csv')
    dataf = clean_data(data)
    skills_data = take_skills(dataf)
    print('data = {')
    for key in skills_data.keys():
        print(f'{key}: {skills_data[key]}', end=',\n')
    print('}')
    # for i in x:
    #     print(', '.join(i))
    # data = ('DevOps ,Linux ,Docker ,PostgreSQL ,Python ,Ansible ,MySQL ,Java ,AWS ,Git ,Zabbix ,Jenkins ,Kubernetes ,CentOS ,Business English ,Gitlab ,KVM ,devops ,Highload ,JavaScript ,Virtualization ,OpenVZ ,RHEL ,SaaS ,Администрирование серверов Linux ,Английский язык ,Bash ,Cloud ,C# ,PHP ,CI/CD ,SQL ,Ruby ,work from home ,Nginx ,C++ ,remote work ,Devops ,docker ,HTML ,Software Development ,CSS ,Scrum ,NoSQL ,ORACLE ,Agile Project Management ,aws ,saasops ,remote ,.NET Framework ,TDD ,Engineering ,MongoDB ,Azure ,REST ,Terraform ,SOA ,EDA ,ООП ,engineer ,Spring Framework ,VMware ,Prometheus ,network ,Rest (API) ,cloud ,TCP/IP ,React ,Networking ,Architecture ,Redis ,Cloud Computing ,nspawn ,MS SQL ,software ,sre ,Puppet ,Symfony ,system administration ,iaas ,paas ,cloud computing ,orchestration ,system admin ,cloud migration ,TeamCity ,Atlassian Jira ,AngularJS ,Laravel ,IaC ,Perl ,ELK ,Unix ,HTML5 ,architect ,Java EE ,CSS3 ,Grafana ,ansible ,Ruby On Rails ,systems ,MS SQL Server ,TFS ,Project management ,Kafka ,Helm ,Chef ,Node.js ,RabbitMQ ,SLA ,kubernetes ,QA ,SQL Server ,azure ,PowerShell ,Databases ,it operations ,site reliability ,site reliability engineering ,reliability engineer ,cloud applications ,cloud architect ,manager ,Visual Studio Net ,MSSQL ,HTTP ,Amazon Web Services ,IT Recruitment ,IT ,Backend ,Memcached ,English ,CI ,software engineering manager ,SDLC ,GitLab ,SRE ,Amazon ,Администрирование серверов Windows ,Design Patterns ,ASP.NET ,Shell Scripting ,Базы данных ,administration ,Golang ,CD ,Apache Tomcat ,Web Services ,Microsoft Visual Studio ,web services ,Yii ,Debian ,Cassandra ,jQuery ,Apache Maven ,Windows Server ,Consul ,GitOps ,salt ,vagrant ,Hadoop ,Nagios ,Active Directory ,Работа в команде ,Elasticsearch ,C/C++ ,ibm cloud ,API ,.NET Core ,ReactJS ,Azure DevOps Server ,MS Visual Studio ,.NET ,crossover ,Администрирование сетевого оборудования ,Cloud Architecture ,Business Development ,Azure DevOps ,Phyton ,openstack ,Unix Shell Scripts ,Apache HTTP Server ,it ,Bootstrap ,Entity Framework ,openvz ,Product Management ,Unit Testing ,Team management ,IIS ,mssql ,JPA ,JS Framework ,Angular2 ,Angular ,Управление качеством ,Cisco ,Continuous Integration ,Django Framework ,MVC ,Test Automation ,Administrator ,System Administration ,terraform ,Gitlab CI ,VPN ,Relational DBs ,Product Manager ,IT Product Manager ,JavaScript Framework ,Amazon Aurora ,Big Data ,CRM ,CROSSOVER ,XML ,Analytical skills ,EFK ,spring ,Octopus ,chef ,Настройка DNS ,EC2 ,Информационная безопасность ,Vice President ,ITSM ,ORM ,Разработка CMS ,Lotus Symphony ,Zipkin ,Jagger ,NixOS ,Ubuntu Server ,awk ,amazon ,Windows ,Lambda ,Веб-программирование ,Remote Work ,Bug Tracking Systems ,Ceph ,Функциональное тестирование ,СУБД ,ASP.NET Core ,Customer Service ,devops tools ,grafana ,Test case ,Управление проектами ,Agile ,Коммуникабельность ,Cloud Arhitecture ,IT Operations ,Quality Control ,ClickHouse ,Kanban ,Настройка серверов Apache ,Tech Ops ,Frontend ,Системное мышление ,Системный анализ ,Developer ,Apache Spark ,Jira ,PHP5 ,CloudFormation ,it engineer ,CloudFront ,Crossover ,Hyper-V ,SCALA ,TypeScript ,Java SE ,gitlab ,Microservices ,chief ,Testing Framework ,ITIL ,Presentation skills ,microservices ,Тестирование ,Go ,Выявление требований ,Управление требованиями ,Документирование требовапний ,Проектирование предметной области ,Прототипирование ,Моделирование процессов ,Разработка технических заданий ,IPTables ,Software Engineer ,DSL networks ,Cloud migration ,Разработка ПО ,Google Cloud Platform ,Удаленная работа ,Web Application Development ,Техническая поддержка ,DevOPs ,it developer ,Внедрение систем информационной безопасности ,Flask ,SOA, EDA, Design Patterns ,SaasOps ,Business Management ,VP ,Http Proxy ,Atlassian Confluence ,Kibana ,Oracle Pl/SQL ,RDS ,Saasops ,REST API ,Teamleading ,Quality Management ,QA Engineer ,QA Manager ,Negotiation skills ,Leadership Skills ,Groovy ,Scripting ,Apache ,Swagger ,XUnit ,S3 ,Ubuntu ,Blazor ,Cистемы управления базами данных ,QA Manual ,Microsoft Azure DevOps ,ALM (Quality Center) ,Zephyr ,Xray ,Agile/Scrum ,Development ,Business Process Management ,Information Security ,OpenStack ,Manager ,English, Remote Work ,AWS Elastic Beanstalk ,VPC ,Администрирование серверов ,Аудит безопасности ,Kotlin ,Cisco CCNP level ,Mikrotik RoutersOS ,UbiquityLinux/Unix ,NetDevOps ,APIs ,FreeBSD ,highload ,Fullstack ,SOLID ,DRY ,PXE ,Тестирование пользовательского интерфейса ,Back-end ,RoR ,DNS ,ElasticSearch ,GCP ,Blockchain ,Cloud computing ,System architecture ,YAML ,alertmanager ,exporters ,promQL ,Amazon AWS ,1С программирование ,Администрирование ,SEM ,LAMP ,Redmine ,JUnit ,Средства криптографической защиты информации ,DynamoDB ,Vagrant ,SAP ,Ajax ,PHP7 ,google cloud ,Troubleshooting ,Route53 ,OOP ,Information Technology ,MS SharePoint ,Openstack ,1С: Предприятие 8 ,PaaS ,Software Engineering manager ,reactjs ,Виртуализация ,Docker Swarm ,Google Cloud ,backend ,ssh ,Алгоритмы ,Multithread Programming ,collectd ,lxc ,proxmox ,системы мониторинга ,хостинг ,absible ,foreman ,Helpdesk ,BPMN ,Проведение тестирований ,LDAP ,Hardware ,Tomcat ,Kubernetis ,Open Stack Swift (OSS) ,Solaris ,WCF ,Serverless ,База данных: Oracle ,Информационные технологии ,BDD ,CI\CD ,TCP ,NUnit ,Hotfix ,Windows Server 2012/2016 ,Android ,PyTest ,Data Science ,Hashicorp Vault ,Разговорный английский ,Управление персоналом ,gentoo ,Maven ,Java EE, SQL server,Oracle,MySQL, Cloud Computing, Linux, DevOps ,English is a must ,NHibernate ,Proxmox ,Nexus ,JSON API ,CloudFlare ,Virtual Private Cloud ,DDoS Protection ,Антивирусная защита сети ,Aurora ,Технические средства информационной защиты ,Администрирование сайтов ,RDBMS ,Redux ,programmer ,UWP ,Spark ,1С-Битрикс ,blockchain ,InstallShield ,FinalBuilder ,Management ,Computer Science ,Organization ,Operations ,InfrasoftCAD ,IBM Cloud ,Java Manager ,People Management ,Java Architecture ,Настройка сетевых подключений ,Управление разработкой ,machine learning ,ML ,PMI ,Системная интеграция ,системное администрирование ,Ведение переговоров ,Continuous Delivery ,CMS Wordpress ,SVN ,Remote ,CTO ,Моделирование бизнес процессов ,Elixir ,Нагрузочное тестирование ,Selenium ,Тестирование мобильных приложений ,Тестирование Web API ,Тестирование web-приложений ,EKS ,Celery ,MS Silverlight ,.NET CORE ,Swift ,Работа с базами данных ,Frontend API ,Teambuilding ,prometheus ,Управление командой ,gRPC ,Protobuf ,Low-latency ,FIX ,Алготрейдинг ,Трейдинг ,Блокчейн ,xUnit ,CLR ,ReactiveX ,Kuternetes ,OpenShift ,Vault ,руководство командой разработчиков ,Навыки презентации ,Лидерство ,Автоматизация процессов ,selenium ,Консультирование ,Computer Vision ,ECS ,Auto Scaling ,DeVops ,Tarantool ,Unity ,Разработка компьютерных Игр ,Teamplayer ,SysOps ,Stash ,high load ,Monitoring ,Atlassian ,Software ,Eglish ,Software Engineering ,Usability ,Java, .NET, Cloud, DevOps, Agile, SDLC, SLA, AWS, TDD ,UI ,software developer ,Bugzilla ,Varnish ,Подбор персонала ,SAP ERP ,Web Design ,WEB аналитика ,E-Staff ,AXAPTA ,ES6 ,react ,администрирования Linux ,администрирования Windows ,администрирования баз данных ,Xen ,Windows 10 ,Intune ,VNC ,Развертывание ,Windows Server 2003 ,Настройка VPS/VDS серверов ,Настройка почтовых серверов ,Серверное программирование ,WebAPI ,Socket.IO ,Экспертный аудит информационных систем ,CSSLP ,Infowatch ,Проектирование ,linux shell ,Github ,Slack ,Mac Os ,Magento ,Meteor ,Techops ,KPI ,Executive ,bitcoin ,Office 365 ,Проектирование пользовательских интерфейсов ,Автоматизация медицинских процессов ,Медицинская документация ,Документирование информационных систем ,IDEF ,Backend-разработка (Erlang, Node.js, Python, PostgreSQL) ,devops engineering (Ansible, Continuous Delivery, Server Infrastructure) ,Microservice ,Rocket.Chat ,ChatOps ,Чувство юмора ,Vue.js ,Transact-SQL ,Маршрутизация трафика ,CMake ,Access ,VCS ,Objective-C ,iOS ,Typescript ,Clouds ,Bit bucket ,Oracle 11G ,Google Docs ,Skype ,Clickhouse ,Apache Flink ,Druid ,Pinot ,Presto ,Apache Pulsar ,Apache Kafka ,HA proxy ,Microsoft Azure ,Azure Devops ,STL ,opencv ,Аналитика ,разработка ,Data Mining ,Математическая статистика ,R&D ,Administrative Support ,Infrastructure ,GOlang ,JS ,Integration Testing ,MS SSRS ,SignalR ,CI/СD ,WPF ,Обучение и развитие ,Грамотная речь ,PotgreSQL ,Способность обучать других ,Умение принимать решения ,DevOps practices ,k8s ,rust ,webassembly ,Azure Services ,Azure Oauth, APIM, FrontDoor ,Azure Search ,Azure Security ,Azure Monitoring ,Azure Cloud: ,DevOps Azure ,Мониторинг ,ERP ,Windows Forms ,Оптимизация бизнес-процессов ,1C:ERP ,1C:УХ ,Бизнес-моделирование ,IT-консалтинг ,Функциональная аналитика ,Анализ бизнес-процессов ,Разработка проектного решения ,Моделирование архитектуры системы ,LVM ,Corosync ,Pacemaker ,devOps ,SOAP ,разработка архитектуры ,разработка инфраструктуры компании ,CD\CI ,Информационный безопасности ,кибератак ,ИБ ,расследование инцидентов ИБ ,Создание концепции ИБ ,DevOps. ,Резервное копирование ,Аудит ИТ инфраструктуры ,MS Office ,Machine Learning ,Lua ,Data Analysis ,Distributed Systems ,Images Processing ,Algorithms & Data Structures ,Deep Learning ,Machine Learning Data Science ,PyTorch ,SMTP/POP3/IMAP ,CloudWatch ,Высоконагруженные системы ,Android SDK ,DevSecOps ,kafka ,elasticsearch ,обработка облачных данных ,Cloud API ,удаленная работа ,Go, DevOps ,Alertmanager ,Jaeger ,Fluent English ,Cloud architect ,English: Intermediate+ ,SOLID principles ,Clean code ,Architecture patterns ,IoC tools ,Fully remote job ,oVirt ,OpenNebula ,K8S ,Tensorflow ,OpenCV ,runtime ,unit ,Регрессионное тестирование ,Критическое мышление ,Формирование команды ,Payments ,VoIP ,System administration ,RunDeck ,Bamboo ,CloudStack ,Front-End development ,shell commnads ,Системы мониторинга ,Cacti ,DHCP ,gpo ,Microsoft Windows Server ,LXC ,GNS3 ,автоматизация разработки ПО ,облачные технологии ,Full-stack ,PHP/FPM ,Agile, Cloud, SDLC, DevOps, SLA, AWS, TDD, Remote Work, Global ,English, Cloud, Agile, SDLC, SLA, AWS, TDD, DevOps, Remote Work, Global ,Agila, SDLC, SLA, AWS, TDD, Cloud, DevOps, Java, .NET ,Java, .NET, Agile, Cloud, SDLC, SLA, DevOps, AWS, TDD ,Java, .Net, Cloud, Agile, DevOps, SDLC, SLA ,администрирование web-проектов ,OSI ,Customer Support ,JDBC ,Hibernate ORM ,DB2 ,Liquibase ,Cucumber ,Ext JS ,VueJS ,High-Load ,Fault-Tolerant ,Auror ,Work from Home ,Software Architect ,Software Developer ,Windows 7 ,IT development ,it software development ,it engineering ,it software ,hadoop ,hive ,Build engineer ,MSBuild ,Sphinx ,WSO2 ,Atlassian Bitbucket ,Logstash ,TypeORM ,Sass ,scss ,Webpack ,react.js ,ГИС ,delivery ,relocate ,VirtualBox ,configuration manager ,Http Server ,Mac Os X Server ,Настройка ПК ,Настройка ПО ,Настройка серверов ,Сборка ПК ,Communication skills ,Deploy ,Continuous Deployment ,Автоматизация тестирования ,Системное администрирование ,https ,oauth ,Dockerhub ,Memcache ,Springboot ,angular.js ,Cloud Technologies ,SSO ,SAML ,dlink ,Бизнес-анализ ,AWT ,Организаторские навыки ,Архитектор ,Облачные решения ,Cloud foundary ,Solution architect ,Микросервисы ,Amazon web services ,IT Infrastructure ,IBM Websphere ,Микросервисная архитектура ,RedHat ,DBA ,SIP ,Битрикс ,Continious Integration ,SCons ,GNU Make ,TechOps ,PagerDuty ,GitHub ,Ms Exchange Server ,Express Route ,ops ,CM ,VCM ,software architecture ,Vue ,High Availability ,Site Reliability ,Site Reliability Engineer ,MS Teams ,CFD ,гидродинамика ,физика ,Программирование ,CAD ,Регресcионное тестирование ,сисадмин ,Желание обучаться ,Изучать Linux ,Умение находить общий язык с коллегами и клиентами ,Стать DevOps ,Lavarel ,GCE ,Elastic ,webpack ,Ramda ,npm ,Microsoft Windows 7/8/10 ,Microsoft Server 2008/2012/2016 ,ITIL/COBIT, методологии DevOps ,YAGNI ,KISS ,VMs ,APM Civil Engineering ,Vice, president, executive, saasops, IT Operations, IT Infrastructure, Devops, IaaS, PaaS, SaaS, rem ,Red Hat ,OpenShift Container Platform ,JSDoc ,DevOps / CI ,Написание автотестов ,VBA ,pl/sql ,phyton ,OMS ,Azure Security Center ,Azure Monitor ,Mercurial ,phpMyAdmin ,ansilbe ,Socket.io ,Sentry ,Microsoft Dynamics 365 ,MS DevOps ,NonSQL ,Web Fullstack ,CQRS ,.Net Core ,Azure Cloud Services ,Distributed data services ,JS framework ,Внутренний аудит информационных систем ,Внешний аудит информационных систем ,Администрирование, модификация и компиляция Linux ,D-Link ,Mikrotik ,1С ,PROXMOX ,DevOps -инженер ,Поддержка внутренней инфраструктуры ,kubernets ,система мониторинга ,typescript ,Деловая коммуникация ,windows 10 ,octopus deploy ,helm ,программирование ,techlead ,ASP.NET MVC ,WEB API ,Azure Cloud ,Service Bus ,Key Vault ,AppInsights ,NGXS ,NGRX ,SCSS ,Архитектор ПО ,MS Build ,Spectflow ,Rider ,БЛОКЧЕЙН ,MS Project ,Внутренние коммуникации ,Аналитическое мышление ,Администрирование СУБД ,Business Planning ,Swagger UI / API ,Redux js ,Infrastructure management ,go ,drone ,zombie ,websocket ,amazon web services ,Visual Studio C# ,.Net/.Net Core ,ASP.Net Core ,Java: Spring ,Vert.X ,DevOps:Nginx ,HAProxy ,OpenVPN ,HLS ,WebRTC ,RTMP ,Video Streaming ,Nodejs ,Kubernete ,MS Dos ,ELK stack ,Логирование ,UML ,банковский проект ,сетевые схемы ,функциональные требования ,Terrasoft CRM ,Bpmonline ,Creatio ,Javascript (ExtJs, Backbone) ,Javascript + LESS (CSS) ,.NET Framework 4.6.2 ,Закупка оргтехники и оборудования ,Контроль исправности оборудования ,laravel ,vue.js ,back-end ,Apple deweloper ,json ,NuxtJS ,PMBOK ,UX ,DOMObject ,Citrix ,процессы CI/CD ,golang ,Release ,Poetry ,RESTful ,FastApi ,nomad ,Написание тестовой документации ,Разработка автоматизированных тестов ,Проведение презентаций ,Консультирование клиентов ,ERP Systems ,Подготовка презентаций ,Деловое общение ,Разработка инструкций ,Use Case Analysis ,Senior ,Elasticseacrh ,F# ,Управленческие навыки ,Управленческая отчетность ,1С: CRM ПРОФ ,Проведение опросов ,Аналитические исследования ,Product Development ,С# ,NET ,Django ,GitLab CI ,Удаленная диагностика неисправностей рабочих станций ,Обучение пользователей ,Terminal Server ,Computer troubleshooting ,PC Hardware ,Delphi ,внедрение ПО ,Backup and Recovery ,SSH ,IT Management ,App Engine ,Kubernetes Engine ,Cloud Storage ,Cloud SQL ,Azure DevOps\TFS ,galera ,mariabackup ,perkona tools ,web-программирование ,Рефакторинг кода ,Jetbrains Phpstorm ,Аналитические способности ,Руководство коллективом ,Битрикс 24 ,TerraForm or CloudFormation ,ELB ,Kinessis ,REDIS/MemCache ,CI/CD (focus on CD) of either Jenkins or CodePipeline ,Experienced with Identities – Active Directory, SAML, SSO, Cognito ,EKS and ECS for containers ,Мониторинг и логирование ,Observability ,OWASP ,Google ,Pipeline ,Security ,devOps-инженер ,Bitbucket ,GameDev ,Game Programming ,Splunk ,SQL DBs ,IoT ,Web ,SDKs ,Решение проблем ,Windows Os ,Conan ,QBS ,Qt ,C ,Pytest ,puppeteer ,Foreman ,Технический директор ,Payment Systems ,Банковское ПО ,Kubernets ,Преподаватель ,Преподавание ,Широкий кругозор ,HA ,Nomad ,High availability ,WinCC ,InTouch ,VBS ,настрой на развитие навыков ,виртуализация ,BLE ,NFC ,Application development ,системный администратор ,AWS Cloud ,AWS CDK ,SDL ,Знание компьютера ,Хорошая память ,Высокая скорость печати ,Логика ,Поиск информации ,Fargate ,CDK ,ExpressJS ,Wiki ,node ,nest ,nest.js ,разработчик ,Spring Boot ,Azur DevOps ,NLP ,Алгоритмы и структуры данных ,Solidity ,Devsecops ,CSPM ,AWS Config ,AWS Firewall Manager ,AWS Detective ,AWS GuardDuty ,AWS WAF ,Cloud Security ,AWS Cloudformation').split(' ,')
    # print(data)
    # data = map(lambda x: f'<li  class="list-group-item">{x}</li>', data)

# print(''.join(data))





def take_skills(main_data):
    data = []
    data_dict = {}

    for vacancy in main_data:
        for skill in vacancy['key_skills']:
            if not data_dict.__contains__(vacancy['published_at'][:4]):
                data_dict[vacancy['published_at'][:4]] = {skill: 1}
            else:
                if skill not in data_dict[vacancy['published_at'][:4]]:
                    data_dict[vacancy['published_at'][:4]][skill] = 1
                else:
                    data_dict[vacancy['published_at'][:4]][skill] += 1
    for skill in data_dict:
        data.append([skill, data_dict[skill]])
    for key in data_dict.keys():
        data_dict[key] = dict(sorted(data_dict[key].items(), key=lambda x: x[1], reverse=True)[:10])
    return data_dict





def read_file(name):
    flag = True
    counter = 0
    data = []
    with open(name, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        heading = next(reader)
        data.append(heading)
        for row in reader:
            for piece in row:
                if len(piece) == 0:
                    flag = False
                counter += 1
            if flag and (len(heading) == counter):
                data.append(row)
            flag = True
            counter = 0
    return data




def clean_data(data):

    heading = data[0]
    chk_pat = '(?:{})'.format(
        '|'.join(['c#', 'c sharp', 'шарп', 'с#']))

    alfa = data
    alfa.pop(0)
    data_new = []

    for row in alfa:
        dict_new = {}
        for i in range(0, len(heading)):
            if heading[i] == 'key_skills':
                dict_new[heading[i]] = row[i].split("\n")
            else:
                row[i] = row[i].replace("\n", ", ")
                row[i] = row[i].strip()
                dict_new[heading[i]] = row[i]
        #print(f'{date} in {row[5][:4]}')

        if re.search(chk_pat, row[1].lower(), flags=re.I):
       # if (row[1].lower().__contains__('java') or row[1].lower().__contains__('джава') or row[1].lower().__contains__('ява')) and str(date) == row[5][:4]:
            data_new.append(dict_new)
    return data_new


if __name__ == "__main__":
    main()
