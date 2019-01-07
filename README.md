Taiga contrib DingTalk auth
=========================

[![Kaleidos Project](http://kaleidos.net/static/img/badge.png)](https://github.com/kaleidos "Kaleidos Project")
[![Managed with Taiga.io](https://img.shields.io/badge/managed%20with-TAIGA.io-709f14.svg)](https://tree.taiga.io/project/taiga/ "Managed with Taiga.io")

该项目继承自[taiga-contrib-gitlab-auth](https://github.com/taigaio/taiga-contrib-gitlab-auth)
钉钉相关资源链接：[用户管理](https://open-doc.dingtalk.com/microapp/serverapi2/ege851), [扫码登录第三方Web网站](https://open-doc.dingtalk.com/microapp/serverapi2/kymkv6), [免登相关API](https://open-doc.dingtalk.com/microapp/serverapi2/athq8o)

### 准备工作
1. 需要在[钉钉开放平台](https://open-dev.dingtalk.com)的【应用开发】-->【开发信息】-->【开发授权】-->【新增授权】，添加【通讯录只读权限】；
2. 需要准备corp_id，corp_secret，app_id，app_secret；
3. 根据钉钉要求，需要将Taiga服务器公网IP填写到白名单中；

### 注意
1. 通过钉钉扫码二维码登录Taiga，如果Taiga系统中当前用户不存在，则创建（前提是钉钉通讯录中存在）；
2. 新添加的用户不属于任何项目，需要通过邀请添加。

Installation
------------

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-dingtalk-auth/back
  workon taiga
  pip install -e .
```

Modify `taiga-back/settings/local.py` and include the line:

```python
  INSTALLED_APPS += ["taiga-contrib-dingtalk-auth"]

  DINGTALK_APP_ID = "YOUR-DINGTALK-APP-ID"
  DINGTALK_APP_SECRET = "YOUR-DINGTALK-APP-SECRET"
  DINGTALK_CORP_ID = "YOUR-DINGTALK-CORP-ID"
  DINGTALK_CORP_SECRET = "YOUR-DINGTALK-CORP-SECRET"

  DINGTALK_URL="https://oapi.dingtalk.com"

```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-dingtalk-auth/front/dist dingtalk-auth
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/dingtalk-auth/dingtalk-auth.json"`:

```json
...
    "dingtalkAppID": "DingTalk_APP_ID",
    "contribPlugins": [
        (...)
        "/plugins/dingtalk-auth/dingtalk-auth.json"
    ]
...
```

In the plugin source dir `taiga-contrib-dingtalk-auth/front` run

```bash
sudo npm install -g gulp
npm install
gulp build
```
