<template>
  <div class="opt-more absolute right-[12px] top-0" v-clickoutside="handleClickOutside">
    <bk-dropdown
      trigger="manual"
      :is-show="dropdownVisible"
    >
      <span
        class="user-icon icon-more !leading-[32px] p-[2px] hover:bg-[#DCDEE5] rounded-[2px]"
        @click="dropdownVisible = !dropdownVisible">
      </span>
      <template #content>
        <bk-dropdown-menu>
          <bk-dropdown-item
            v-for="item in deptDropdownList"
            :key="item.name"
            @click.prevent="item.action(dept)"
          >
            {{ item.name }}
          </bk-dropdown-item>
          <div v-if="!isCollaboration">
            <div class="border-t border-[#EAEBF0] mx-[12px] my-[4px]"></div>
            <bk-dropdown-item
              @click.prevent="handleDelete"
            >
              {{ $t('删除组织') }}
            </bk-dropdown-item>
          </div>
        </bk-dropdown-menu>
      </template>
    </bk-dropdown>


    <bk-dialog
      :is-show="orgDialogVisible"
      :title="isAddSubOrg ? $t('添加子组织') : $t('重命名')"
      height="200"
      @closed="orgDialogVisible = false"
      @confirm="handleOrg"
    >
      <bk-form form-type="vertical" class="mt-[10px]">
        <bk-form-item
          :label="$t('组织名称')"
          :required="true"
        >
          <bk-input v-model="deptName"></bk-input>
        </bk-form-item>
      </bk-form>
    </bk-dialog>

    <!-- 移至目标组织弹框 -->
    <bk-dialog
      :is-show="moveDialogShow"
      :title="$t('移至目标组织')"
      :theme="'primary'"
      :size="'normal'"
      @closed="() => moveDialogShow = false"
      @confirm="() => confirmOperations()"
    >
      <div class="mb-[16px] text-[#979BA5]">{{moveTips}}</div>
      <bk-form class="example" form-type="vertical">
        <bk-form-item :label="$t('选择组织')">
          <bk-select
            v-model="selectedValue"
            class="bk-select"
            filterable
            auto-focus
            :clearable="false"
            id-key="id"
            display-key="name"
            collapse-tags
          >
            <bk-option
              v-for="item in dataSource"
              :key="item.id"
              :id="item.id"
              :name="item.name"
              :disabled="disabledDept(item.id)"
              v-bk-tooltips="{ content: $t('已在当前部门'), disabled: !disabledDept(item.id), boundary: 'parent' }"
            />
          </bk-select>
        </bk-form-item>
      </bk-form>
    </bk-dialog>
  </div>
</template>


<script setup lang="ts">
import { clickoutside as vClickoutside, InfoBox } from 'bkui-vue';
import { computed, h, ref } from 'vue';

import { addDepartment, deleteDepartment, dragOrg, optionalDepartmentsList, updateDepartment } from '@/http/organizationFiles';
import { t } from '@/language/index';
import router from '@/router';

const props = defineProps({
  dept: {
    type: Object,
    default: () => ({}),
  },
  tenant: {
    type: Object,
    default: () => ({}),
  },
  isCollaboration: {
    type: Boolean,
    default: false,
  },
});

const emits = defineEmits(['updateNode', 'addNode', 'deleteNode', 'moveNode']);

const deptName = ref(props.dept.name);
const disabledDept = computed(() => id => props.dept?.__attr__?.parent?.id === id);

const dropdownVisible = ref(false);

const orgDialogVisible = ref(false);
const isAddSubOrg = ref(false);
const moveDialogShow = ref(false);
const selectedValue = ref('');
const dataSource = ref([]);
const moveTips = ref('');
const moveOrg = ref('');

const defaultDropdownList = ref<any[]>([
  {
    name: t('添加子组织'),
    action: () => {
      dropdownVisible.value = false;
      isAddSubOrg.value = true;
      orgDialogVisible.value = true;
      deptName.value = '';
    },
  },
  {
    name: t('移至目标组织'),
    action: async (item) => {
      dropdownVisible.value = false;
      isAddSubOrg.value = false;
      orgDialogVisible.value = false;
      moveDialogShow.value = true;
      const res = await optionalDepartmentsList();
      dataSource.value = res.data;
      moveOrg.value = item.id;
      moveTips.value = `${t('将')}${item.name}${t('从当前组织移出')}, ${t('并追加到以下组织')}`;
    },
  },
  {
    name: t('重命名'),
    action: () => {
      dropdownVisible.value = false;
      isAddSubOrg.value = false;
      orgDialogVisible.value = true;
      deptName.value = props.dept.name;
    },
  },
]);

const collaborationDropdownList = ref<any[]>([
  {
    name: t('协同配置'),
    action: () => {
      router.push({
        name: 'collaboration',
        query: {
          tab: 'other',
        },
      });
    },
  },
]);

const deptDropdownList = computed(() => (props.isCollaboration
  ? collaborationDropdownList.value
  : defaultDropdownList.value));

const handleClickOutside = () => {
  setTimeout(() => {
    dropdownVisible.value = false;
  });
};

/**
 * 删除
 */
const handleDelete = () => {
  dropdownVisible.value = false;
  InfoBox({
    title: t('确认删除该组织？'),
    confirmText: t('确定'),
    subTitle: h(
      'div',
      {},
      [
        h(
          'p',
          {
            style: {
              color: '#313238',
              paddingBottom: '10px',
            },
          },
          `${t('组织')}: ${props.dept.name}`,
        ),
      ],
    ),
    onConfirm: () => {
      deleteDepartment(props.dept.id).then(() => {
        emits('deleteNode', props.dept.id);
      });
    },
  });
};

/**
 * @description 创建租户部门/更新租户部门
 */
const handleOrg = () => {
  orgDialogVisible.value = false;
  if (isAddSubOrg.value) {
    const newOrg = {
      name: deptName.value,
      parent_department_id: props.dept.id,
    };
    addDepartment(props.tenant.id, newOrg).then((res) => {
      const node = {
        id: res.data.id,
        name: deptName.value,
        has_children: false,
      };
      emits('addNode', props.dept.id, node);
    });
  } else {
    updateDepartment(props.dept.id, { name: deptName.value }).then(() => {
      const node = {
        ...props.dept,
        name: deptName.value,
      };
      emits('updateNode', node);
    });
  }
};

/**
 * 移至目标组织
 */
const confirmOperations = async () => {
  try {
    await dragOrg(moveOrg.value, { parent_department_id: selectedValue.value });
    moveDialogShow.value = false;
    emits('moveNode');
  } catch (e) {
    console.warn(e);
  }
};
</script>
