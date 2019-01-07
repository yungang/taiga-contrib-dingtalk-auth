# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import logging
logger = logging.getLogger(__name__)

from collections import namedtuple

from django.conf import settings


######################################################
## Variables from Taiga config front-end/dist/conf.json
######################################################

DINGTALK_APP_ID = getattr(settings, "DINGTALK_APP_ID", None)
DINGTALK_APP_SECRET = getattr(settings, "DINGTALK_APP_SECRET", None)
DINGTALK_CORP_ID = getattr(settings, "DINGTALK_CORP_ID", None)
DINGTALK_CORP_SECRET = getattr(settings, "DINGTALK_CORP_SECRET", None)
DINGTALK_URL = getattr(settings, "DINGTALK_URL", None)

User = namedtuple("User", ["id", "username", "full_name", "bio", "email"])

######################################################
## DingTalk system calls
######################################################

def me(access_code:str, redirectUri:str) -> tuple:
    """
    Connect to DingTalk Open API and get all personal info (profile and the primary email).
    """
    logger.error("~~~~~~~  me access_code " + access_code)
    res_obj = requests.get("https://oapi.dingtalk.com/gettoken?corpid=" + DINGTALK_CORP_ID + "&corpsecret=" + DINGTALK_CORP_SECRET).json()
    logger.error("~~~~~~~  corp access token " + json.dumps(res_obj))
    corp_access_token = res_obj["access_token"]
    res_obj = requests.get("https://oapi.dingtalk.com/sns/gettoken?appid=" + DINGTALK_APP_ID + "&appsecret=" + DINGTALK_APP_SECRET).json()
    logger.error("~~~~~~~  access token " + json.dumps(res_obj))
    access_token = res_obj["access_token"]
    params = {"tmp_auth_code": access_code}
    res_obj = requests.post("https://oapi.dingtalk.com/sns/get_persistent_code?access_token=" + access_token, json=params).json()
    logger.error("~~~~~~~  persistent_code " + json.dumps(res_obj))
    persistent_code = res_obj["persistent_code"]
    logger.error("~~~~~~~  persistent code " + persistent_code)
    params = {"openid": res_obj["openid"], "persistent_code": res_obj["persistent_code"]}
    res_obj = requests.post("https://oapi.dingtalk.com/sns/get_sns_token?access_token=" + access_token, json=params).json()
    logger.error("~~~~~~~  sns token " + res_obj["sns_token"])
    res_obj = requests.get("https://oapi.dingtalk.com/sns/getuserinfo?sns_token=" + res_obj["sns_token"]).json()
    logger.error("~~~~~~~  user info " + json.dumps(res_obj))
    res_obj = requests.get("https://oapi.dingtalk.com/user/getUseridByUnionid?access_token=" + corp_access_token + "&unionid=" + res_obj["user_info"]["unionid"]).json()
    logger.error("~~~~~~~  userid " + json.dumps(res_obj))
    data = requests.get("https://oapi.dingtalk.com/user/get?access_token=" + corp_access_token + "&userid=" + res_obj["userid"]).json()
    logger.error("~~~~~~~  user info by id" + json.dumps(data))

    user = User(id=data.get("unionid", None),
                username=data.get("user_id", None),
                full_name=(data.get("name", None) or ""),
                email=(data.get("email", None) or ""),
                bio=(data.get("extattr", None) or ""))
    return user.email, user
