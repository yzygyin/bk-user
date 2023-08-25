# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-用户管理(Bk-User) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from bkuser.apps.data_source.models import DataSourceDepartment, DataSourceDepartmentUserRelation, DataSourceUser
from bkuser.biz.validators import validate_data_source_user_username
from bkuser.common.validators import validate_phone_with_country_code

logger = logging.getLogger(__name__)


class UserSearchInputSLZ(serializers.Serializer):
    username = serializers.CharField(required=False, help_text="用户名", allow_blank=True)


class DataSourceSearchDepartmentsOutputSLZ(serializers.Serializer):
    id = serializers.CharField(help_text="部门ID")
    name = serializers.CharField(help_text="部门名称")


class UserSearchOutputSLZ(serializers.Serializer):
    id = serializers.CharField(help_text="用户ID")
    username = serializers.CharField(help_text="用户名")
    full_name = serializers.CharField(help_text="全名")
    phone = serializers.CharField(help_text="手机号")
    email = serializers.CharField(help_text="邮箱")
    departments = serializers.SerializerMethodField(help_text="用户部门")

    # FIXME:考虑抽象一个函数 获取数据后传递到context
    @swagger_serializer_method(serializer_or_field=DataSourceSearchDepartmentsOutputSLZ(many=True))
    def get_departments(self, obj: DataSourceUser):
        return [
            {"id": department_user_relation.department.id, "name": department_user_relation.department.name}
            for department_user_relation in DataSourceDepartmentUserRelation.objects.filter(user=obj)
        ]


class UserCreateInputSLZ(serializers.Serializer):
    username = serializers.CharField(help_text="用户名", validators=[validate_data_source_user_username])
    full_name = serializers.CharField(help_text="姓名")
    email = serializers.EmailField(help_text="邮箱")
    phone_country_code = serializers.CharField(
        help_text="手机号国际区号", required=False, default=settings.DEFAULT_PHONE_COUNTRY_CODE
    )
    phone = serializers.CharField(help_text="手机号")
    logo = serializers.CharField(help_text="用户 Logo", required=False)
    department_ids = serializers.ListField(help_text="部门ID列表", child=serializers.IntegerField(), default=[])
    leader_ids = serializers.ListField(help_text="上级ID列表", child=serializers.IntegerField(), default=[])

    def validate(self, data):
        validate_phone_with_country_code(phone=data["phone"], country_code=data["phone_country_code"])
        return data

    def validate_department_ids(self, department_ids):
        diff_department_ids = set(department_ids) - set(
            DataSourceDepartment.objects.filter(
                id__in=department_ids, data_source=self.context["data_source"]
            ).values_list("id", flat=True)
        )
        if diff_department_ids:
            raise serializers.ValidationError(_("传递了错误的部门信息: {}").format(diff_department_ids))
        return department_ids

    def validate_leader_ids(self, leader_ids):
        diff_leader_ids = set(leader_ids) - set(
            DataSourceUser.objects.filter(id__in=leader_ids, data_source=self.context["data_source"]).values_list(
                "id", flat=True
            )
        )
        if diff_leader_ids:
            raise serializers.ValidationError(_("传递了错误的上级信息: {}").format(diff_leader_ids))
        return leader_ids


class UserCreateOutputSLZ(serializers.Serializer):
    id = serializers.CharField(help_text="数据源用户ID")