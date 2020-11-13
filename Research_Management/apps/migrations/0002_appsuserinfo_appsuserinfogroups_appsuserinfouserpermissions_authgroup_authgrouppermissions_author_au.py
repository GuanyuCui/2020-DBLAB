# Generated by Django 3.1.3 on 2020-11-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppsUserinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
                ('create_time', models.DateField()),
            ],
            options={
                'db_table': 'apps_userinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AppsUserinfoGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'apps_userinfo_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AppsUserinfoUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'apps_userinfo_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('authorid', models.CharField(db_column='AuthorID', max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=20)),
            ],
            options={
                'db_table': 'Author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Conferjournal',
            fields=[
                ('name', models.CharField(db_column='Name', max_length=100, primary_key=True, serialize=False)),
                ('conferorjournal', models.CharField(db_column='ConferOrJournal', max_length=1)),
                ('abbreviation', models.CharField(blank=True, db_column='Abbreviation', max_length=50, null=True)),
                ('ruclevel', models.CharField(db_column='RUCLevel', max_length=2)),
                ('ccflevel', models.CharField(db_column='CCFLevel', max_length=2)),
                ('ccfchinalevel', models.CharField(db_column='CCFChinaLevel', max_length=2)),
                ('issn', models.CharField(blank=True, db_column='ISSN', max_length=50, null=True)),
            ],
            options={
                'db_table': 'ConferJournal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pa',
            fields=[
                ('paid', models.IntegerField(db_column='PAID', primary_key=True, serialize=False)),
                ('authorrank', models.IntegerField(db_column='AuthorRank')),
                ('authoridentity', models.CharField(db_column='AuthorIdentity', max_length=20)),
            ],
            options={
                'db_table': 'PA',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('title', models.CharField(db_column='Title', max_length=100, primary_key=True, serialize=False)),
                ('conferorjournal', models.CharField(db_column='ConferOrJournal', max_length=1)),
                ('publishtime', models.DateField(db_column='PublishTime')),
                ('volume', models.IntegerField(blank=True, db_column='Volume', null=True)),
                ('issue', models.IntegerField(blank=True, db_column='Issue', null=True)),
                ('startpage', models.IntegerField(db_column='StartPage')),
                ('endpage', models.IntegerField(db_column='EndPage')),
                ('keywords', models.CharField(blank=True, db_column='Keywords', max_length=100, null=True)),
                ('conferencelocation', models.CharField(blank=True, db_column='ConferenceLocation', max_length=50, null=True)),
                ('language', models.CharField(blank=True, db_column='Language', max_length=10, null=True)),
            ],
            options={
                'db_table': 'Paper',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Papertype',
            fields=[
                ('typeid', models.IntegerField(db_column='TypeID', primary_key=True, serialize=False)),
                ('typename', models.CharField(db_column='TypeName', max_length=20)),
            ],
            options={
                'db_table': 'PaperType',
                'managed': False,
            },
        ),
    ]
