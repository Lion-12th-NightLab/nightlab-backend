"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from auths.views import login,token_reissue #verify
from todos.views import TodoUpdateAndDelete, TodoCheckBox, TodoCreateAndGetAll
from users.views import user_signup, users_list, nickname_check, MypageGetAndUpdate, UserRevoke
from verify.views import SendVerification, CheckVerifycode
from timer.views import timer_start, timer_stop, timer_rest_start, timer_rest_stop
from memo.views import memo, memo_list
from analyze.views import analyze
from main.views import main, onboard


router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="NightLab API",
        default_version='v1',
        description="NightLab API Test",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # auth
    path("auth/kakao/login", login),
    path("auth/kakao/token_reissue", token_reissue),
    path("auth/verify", SendVerification),
    path("auth/verify/check", CheckVerifycode),
    path("auth/signup", user_signup),
    path("auth/check/nickname", nickname_check),

    # timer
    path("api/timer/start", timer_start),
    path("api/timer/stop", timer_stop),
    path("api/timer/rest/start", timer_rest_start),
    path("api/timer/rest/stop", timer_rest_stop),

    # users
    path("api/users/list", users_list),

    # todo
    path("api/todo", TodoCreateAndGetAll),
    path('api/todo/<int:todo_id>', TodoUpdateAndDelete),
    path('api/todo/checkbox/<int:todo_id>', TodoCheckBox),

    # memo
    path("api/memo",memo),
    path("api/memo/all", memo_list),


    # mypage
    path("api/mypage",MypageGetAndUpdate),
    path("api/mypage/revoke",UserRevoke),

    # analyze
    path("api/analyze", analyze),

    #main
    path("api/main", main),
    path("api/onboard", onboard)

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        ]