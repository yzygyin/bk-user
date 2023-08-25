<template>
  <div class="details-info-wrapper user-scroll-y">
    <ul class="details-info-content" v-if="!state.isEdit">
      <li class="content-item">
        <div class="item-header">
          <p class="item-title">基本信息</p>
          <bk-button outline theme="primary" @click="handleClickEdit">
            编辑
          </bk-button>
        </div>
        <ul class="item-content flex" style="width: 72%">
          <li>
            <span class="key">公司名称：</span>
            <span class="value">{{ state.tenantsData.name }}</span>
          </li>
          <li>
            <span class="key">人员数量：</span>
            <span class="value">{{ userNumberVisible }}</span>
          </li>
          <li>
            <span class="key">公司ID：</span>
            <span class="value">{{ state.tenantsData.id }}</span>
          </li>
          <li>
            <span class="key">更新时间：</span>
            <span class="value">--</span>
          </li>
          <li>
            <span class="key">公司状态：</span>
            <span class="value">启用</span>
          </li>
          <img src="@/images/avatar.png" />
        </ul>
      </li>
      <li class="content-item">
        <div class="item-title">管理员</div>
        <bk-table
          class="user-info-table"
          :data="state.tenantsData.managers"
          show-overflow-tooltip
        >
          <bk-table-column prop="username" label="用户名"></bk-table-column>
          <bk-table-column prop="full_name" label="全名"></bk-table-column>
          <bk-table-column prop="phone" label="手机号"></bk-table-column>
          <bk-table-column prop="email" label="邮箱"></bk-table-column>
        </bk-table>
      </li>
    </ul>
    <EditInfo
      v-else
      :tenants-data="state.tenantsData"
      @handleCancel="handleCancel" />
  </div>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue';

import EditInfo from './EditDetailsInfo.vue';

import {
  getTenantDetails,
} from '@/http/tenantsFiles';

const state = reactive({
  isEdit: false,
  tenantsData: {},
});

const userNumberVisible = computed(() => (state.tenantsData?.feature_flags?.user_number_visible ? '显示' : '隐藏'));

const fetchTenantDetails = async () => {
  await getTenantDetails('jianantest').then((res: any) => {
    state.tenantsData = res.data;
  });
};
fetchTenantDetails();

const handleClickEdit = () => {
  state.isEdit = true;
};

const handleCancel = () => {
  state.isEdit = false;
};
</script>

<style lang="less" scoped>
@import url("@/css/tenantViewStyle.less");
</style>