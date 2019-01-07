###
# Copyright (C) 2014-2016 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2016 Jesús Espino Garcia <jespinog@gmail.com>
# Copyright (C) 2014-2016 David Barragán Merino <bameda@dbarragan.com>
# Copyright (C) 2014-2016 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# Copyright (C) 2014-2016 Juan Francisco Alcántara <juanfran.alcantara@kaleidos.net>
# Copyright (C) 2014-2016 Xavi Julian <xavier.julian@kaleidos.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# File: dingtalk-auth.coffee
###

DingTalkLoginButtonDirective = ($window, $params, $location, $config, $events, $confirm,
                              $auth, $navUrls, $loader) ->
    # Login or registar a user with his/her dingtalk account.
    #
    # Example:
    #     tg-dingtalk-login-button()
    #
    # Requirements:
    #   - ...

    link = ($scope, $el, $attrs) ->
        clientId = $config.get("dingtalkAppID", null)

        loginOnSuccess = (response) ->
            if $params.next and $params.next != $navUrls.resolve("login")
                nextUrl = $params.next
            else
                nextUrl = $navUrls.resolve("home")

            $events.setupConnection()

            $location.search("next", null)
            $location.search("token", null)
            $location.search("state", null)
            $location.search("code", null)
            $location.path(nextUrl)

        loginOnError = (response) ->
            $location.search("state", null)
            $location.search("code", null)
            $loader.pageLoaded()

            if response.data._error_message
                $confirm.notify("light-error", response.data._error_message )
            else
                $confirm.notify("light-error", "Our Oompa Loompas have not been able to get you
                                                credentials from DingTalk.")

        loginWithDingTalkAccount = ->
            type = $params.state
            code = $params.code
            token = $params.token

            return if not (type == "dingtalk" and code)
            $loader.start(true)

            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}/login"

            data = {code: code, token: token, redirectUri: redirectUri}
            $auth.login(data, type).then(loginOnSuccess, loginOnError)

        loginWithDingTalkAccount()

        $el.on "click", ".button-auth", (event) ->
            url = document.createElement('a')
            url.href = $location.absUrl()
            redirectToUri = "#{url.protocol}//#{url.hostname}#{if url.port == '' then '' else ':'+url.port}/login"

            #url = "#{auth_url}/oauth/authorize/?client_id=#{clientId}&state=dingtalk&response_type=code&scope=read_user&redirect_uri=#{redirectToUri}"
            url = "https://oapi.dingtalk.com/connect/qrconnect?appid=#{clientId}&response_type=code&scope=snsapi_login&state=dingtalk&redirect_uri=http%3a%2f%2ftaiga.gowild.top%2flogin"
            $window.location.href = url

        $scope.$on "$destroy", ->
            $el.off()

    return {
        link: link
        restrict: "EA"
        template: ""
    }

module = angular.module('taigaContrib.dingtalkAuth', [])
module.directive("tgDingtalkLoginButton", ["$window", '$routeParams', "$tgLocation", "$tgConfig", "$tgEvents",
                                         "$tgConfirm", "$tgAuth", "$tgNavUrls", "tgLoader",
                                         DingTalkLoginButtonDirective])
