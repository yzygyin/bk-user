# Generated by Django 3.2.20 on 2023-08-11 06:57

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='数据源名称')),
                ('owner_tenant_id', models.CharField(db_index=True, max_length=64, verbose_name='归属租户')),
                ('plugin_config', models.JSONField(default=dict, verbose_name='数据源插件配置')),
                ('sync_config', models.JSONField(default=dict, verbose_name='数据源同步任务配置')),
                ('field_mapping', models.JSONField(default=dict, verbose_name='用户字段映射')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DataSourceDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=128, null=True, verbose_name='部门标识')),
                ('name', models.CharField(max_length=255, verbose_name='部门名称')),
                ('extras', models.JSONField(default=dict, verbose_name='自定义字段')),
                ('data_source', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='data_source.datasource')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DataSourcePlugin',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='数据源插件唯一标识')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='数据源插件名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('logo', models.TextField(blank=True, default='', null=True, verbose_name='Logo')),
            ],
        ),
        migrations.CreateModel(
            name='DataSourceUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('full_name', models.CharField(max_length=128, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=32, verbose_name='手机号')),
                ('phone_country_code', models.CharField(blank=True, default='86', max_length=16, null=True, verbose_name='手机国际区号')),
                ('logo', models.TextField(blank=True, default='', max_length=256, null=True, verbose_name='Logo')),
                ('extras', models.JSONField(default=dict, verbose_name='自定义字段')),
                ('data_source', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='data_source.datasource')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('full_name', 'data_source'), ('username', 'data_source')},
            },
        ),
        migrations.AddField(
            model_name='datasource',
            name='plugin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data_source.datasourceplugin'),
        ),
        migrations.CreateModel(
            name='LocalDataSourceIdentityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='用户密码')),
                ('password_updated_at', models.DateTimeField(blank=True, null=True, verbose_name='密码最后更新时间')),
                ('password_expired_at', models.DateTimeField(blank=True, null=True, verbose_name='密码过期时间')),
                ('username', models.CharField(max_length=128, verbose_name='用户名')),
                ('data_source', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='data_source.datasource')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data_source.datasourceuser')),
            ],
            options={
                'unique_together': {('username', 'data_source')},
            },
        ),
        migrations.CreateModel(
            name='DataSourceUserLeaderRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('leader', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='leader', to='data_source.datasourceuser')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='data_source.datasourceuser')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('user', 'leader')},
            },
        ),
        migrations.CreateModel(
            name='DataSourceDepartmentUserRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='data_source.datasourcedepartment')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='data_source.datasourceuser')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('user', 'department')},
            },
        ),
        migrations.CreateModel(
            name='DataSourceDepartmentRelation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='data_source.datasourcedepartment')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('data_source', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='data_source.datasource')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='data_source.datasourcedepartmentrelation')),
            ],
            options={
                'index_together': {('tree_id', 'lft', 'rght'), ('parent_id', 'tree_id', 'lft')},
            },
        ),
    ]