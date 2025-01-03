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

from typing import Any, Optional

from blue_krill.data_types.enum import EnumField, StrStructuredEnum
from django.utils.translation import gettext_lazy as _
from redis.exceptions import LockNotOwnedError  # type: ignore

from bkuser.common.cache import Cache, CacheEnum, CacheKeyPrefixEnum


class LockType(StrStructuredEnum):
    """锁类型"""

    GLOBAL = EnumField("global", label=_("全局锁"))
    DATA_SOURCE_SYNC = EnumField("data_source_sync", label=_("数据源同步锁"))
    TENANT_SYNC = EnumField("tenant_sync", label=_("租户同步锁"))


class RedisLock:
    """基于 Redis 实现的分布式锁"""

    def __init__(self, type_: LockType, suffix: Any = None, timeout: Optional[int] = None, blocking=True) -> None:
        """
        :param type_: 锁类型, LockType 中的值
        :param suffix: 任意实现 __str__ 方法的对象
        :param timeout: 锁超时时间
        :param blocking: 是否为阻塞锁
        """
        key = self._make_key(type_, suffix)
        cache = Cache(CacheEnum.REDIS, CacheKeyPrefixEnum.LOCK)
        self._lock = cache.lock(key, timeout=timeout)
        self._blocking = blocking

    def _make_key(self, type_: str, suffix: Any) -> str:
        """
        生成key
        """
        return f"{type_}:{suffix}" if suffix is not None else type_

    def __enter__(self):
        assert self._blocking
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self) -> bool:
        return self._lock.acquire(blocking=self._blocking)

    def release(self):
        try:
            self._lock.release()
        except LockNotOwnedError:
            pass


def gen_global_lock() -> RedisLock:
    """全局分布式锁，不推荐使用，仅作为示例参考"""
    return RedisLock(LockType.GLOBAL, timeout=5)
