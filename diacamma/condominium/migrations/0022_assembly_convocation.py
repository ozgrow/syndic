from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import PrintModel
import lucterios.framework.model_fields


def printer_model(*_args):
    set_locale_lang(settings.LANGUAGE_CODE)
    PrintModel().load_model("diacamma.condominium", "Notification_0001", is_default=True)


class Migration(migrations.Migration):

    dependencies = [
        ('condominium', '0021_assembly_agenda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assembly',
            name='status',
            field=lucterios.framework.model_fields.FSMIntegerField(choices=[(0, 'in preparation'), (1, 'convened')], db_index=True, default=0, verbose_name='status'),
        ),
        migrations.CreateModel(
            name='AssemblyAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('provided', models.BooleanField(default=False, verbose_name='provided')),
                ('comment', models.TextField(default='', null=True, verbose_name='comment')),
                ('assembly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.assembly', verbose_name='general assembly')),
            ],
            options={
                'verbose_name': 'attachment of notice',
                'verbose_name_plural': 'attachments of notice',
                'ordering': ['assembly', 'id'],
            },
        ),
        migrations.CreateModel(
            name='PostalRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(verbose_name='reception date of the request')),
                ('made_in_assembly', models.BooleanField(default=False, verbose_name='made in general assembly')),
                ('end_date', models.DateField(default=None, null=True, verbose_name='end date')),
                ('comment', models.TextField(default='', null=True, verbose_name='comment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.owner', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'request of postal delivery',
                'verbose_name_plural': 'requests of postal delivery',
                'ordering': ['-request_date'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.IntegerField(choices=[(0, 'notice of meeting'), (1, 'minutes')], default=0, verbose_name='kind')),
                ('channel', models.IntegerField(choices=[(0, 'qualified electronic registered letter'), (1, 'registered letter with acknowledgement of receipt'),
                                                         (2, 'hand delivery against signature'), (3, 'simple e-mail (information only)')], default=0, verbose_name='channel')),
                ('sent_date', models.DateField(default=None, null=True, verbose_name='sending or delivery date')),
                ('presentation_date', models.DateField(default=None, null=True, verbose_name='first presentation date')),
                ('reference', models.CharField(blank=True, default='', max_length=100, verbose_name='reference')),
                ('comment', models.TextField(default='', null=True, verbose_name='comment')),
                ('assembly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.assembly', verbose_name='general assembly')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.owner', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'ordering': ['assembly', 'kind', 'id'],
            },
        ),
        migrations.RunPython(printer_model),
    ]
