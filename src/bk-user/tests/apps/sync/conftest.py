# -*- coding: utf-8 -*-
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - 用户管理 (bk-user) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.

import base64
import io

import pytest
from bkuser.apps.sync.constants import SyncTaskStatus, SyncTaskTrigger
from bkuser.apps.sync.models import DataSourceSyncTask, TenantSyncTask
from django.conf import settings
from django.utils import timezone
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook


@pytest.fixture
def data_source_sync_task(bare_local_data_source) -> DataSourceSyncTask:
    """数据源同步任务"""
    return DataSourceSyncTask.objects.create(
        data_source=bare_local_data_source,
        status=SyncTaskStatus.PENDING,
        trigger=SyncTaskTrigger.MANUAL,
        operator="admin",
        start_at=timezone.now(),
        extras={"overwrite": True, "incremental": False, "async_run": False},
    )


@pytest.fixture
def tenant_sync_task(full_local_data_source, default_tenant, data_source_sync_task) -> TenantSyncTask:
    """租户数据同步任务"""
    return TenantSyncTask.objects.create(
        tenant=default_tenant,
        data_source=full_local_data_source,
        data_source_owner_tenant_id=full_local_data_source.owner_tenant_id,
        data_source_sync_task_id=data_source_sync_task.id,
        status=SyncTaskStatus.PENDING,
        trigger=SyncTaskTrigger.MANUAL,
        operator="admin",
        start_at=timezone.now(),
        extras={"async_run": False},
    )


@pytest.fixture
def user_workbook() -> Workbook:
    return load_workbook(settings.BASE_DIR / "tests/assets/fake_users.xlsx")


@pytest.fixture
def encoded_file(user_workbook) -> str:
    with io.BytesIO() as buffer:
        user_workbook.save(buffer)
        content = buffer.getvalue()

    return base64.b64encode(content).decode("utf-8")
