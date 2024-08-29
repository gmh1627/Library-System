# Library System

### 架构

B/S:Python+Django(后端) + MySql（数据库） + Bootstrap（前端）

### 部署流程

- 运行`pip install Django`安装对应的包

- 修改数据库配置文件`\Library\manage.py`中数据库配置文件

  - 在mysql中创建`library`数据库

  - 找到本地数据库一个可用的管理员账号和密码（当然也可以再注册一个新的）

  - 修改`\Library\settings.py`中以下配置

    ```Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',  # 数据库主机
            'PORT': ,  # 数据库端口
            'USER': '',  # 数据库用户名
            'PASSWORD': '',  # 数据库用户密码
            'NAME': 'library'  # 数据库名字
        }
    }
    ```

- 运行项目

  - 首先执行`pip install mysqlclient`，并保证django已经成功连上数据库
  - 在终端中运行命令`python manage.py runserver`
  - 如果看到白字提示已经运行在`localhost:8000`则提示成功，可用点击进入网站

- 创建管理员账号

  - 运行命令`python manage.py createsuperuser`创建超级用户
  - 运行命令`python manage.py runserver`
  - 进入超级管理员页面`localhost:8000/admin`，用超级用户的用户名和密码登录，添加管理员，并设置密码

- 数据库迁移（在修改了models.py时需要执行）

  - 修改`models.py`
  - 运行命令`python manage.py makemigrations`创建迁移文件
  - 运行命令`python manage.py migrate`进行迁移

- 修改数据库中的数据

  - 可以通过网站相关操作修改
  - 可以直接用过MySQL修改（如删除用户）

### Django框架

- `Library`
  - `settings.py`：配置文件
  - `urls.py`：浏览器中的路径和`views.py`中函数的对应
- `MyWEB`
  - `models.py`：MySQL中表格的定义
  - `views.py`：全部后端逻辑
  - `templates`：存放所有html的文件夹

- `static(存放项目的静态文件)`
  - css:CSS 文件
  - bootstrap:bootstrap框架相关CSS和JavaScript代码
  - img:图片文件
  - zico:为CJK汉语用户设计的图标LOGO系统
