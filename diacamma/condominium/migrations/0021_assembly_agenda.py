from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion

from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import PrintModel
import lucterios.framework.model_fields


def printer_model(*_args):
    set_locale_lang(settings.LANGUAGE_CODE)
    PrintModel().load_model("diacamma.condominium", "Assembly_0001", is_default=True)


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_length_field'),
        ('condominium', '0020_propertylot_maxvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assembly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=None, null=True, verbose_name='date')),
                ('hour', models.TimeField(default=None, null=True, verbose_name='hour')),
                ('place', models.CharField(blank=True, default='', max_length=200, verbose_name='place')),
                ('type_assembly', models.IntegerField(choices=[(0, 'ordinary'), (1, 'extraordinary')], default=0, verbose_name='type of assembly')),
                ('status', lucterios.framework.model_fields.FSMIntegerField(choices=[(0, 'in preparation')], db_index=True, default=0, verbose_name='status')),
                ('comment', models.TextField(default='', null=True, verbose_name='comment')),
            ],
            options={
                'verbose_name': 'general assembly',
                'verbose_name_plural': 'general assemblies',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, null=True, verbose_name='numeros')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('text', models.TextField(default='', null=True, verbose_name='draft resolution')),
                ('kind', models.IntegerField(choices=[(0, 'decision'), (1, 'information (no vote)')], default=0, verbose_name='kind')),
                ('majority', models.IntegerField(choices=[(0, 'article 24 (majority of votes cast)'), (1, 'article 25 (majority of all votes)'), (2, 'article 26 (double majority)'), (3, 'unanimity')], default=0, null=True, verbose_name='majority')),
                ('request_date', models.DateField(default=None, null=True, verbose_name='request date')),
                ('comment', models.TextField(default='', null=True, verbose_name='internal note')),
                ('assembly', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='condominium.assembly', verbose_name='general assembly')),
                ('distribution_key', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='contacts.customfield', verbose_name='distribution key')),
                ('requested_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='condominium.owner', verbose_name='requested by')),
            ],
            options={
                'verbose_name': 'agenda item',
                'verbose_name_plural': 'agenda items',
                'ordering': ['assembly', 'num', 'id'],
            },
        ),
        migrations.RunPython(printer_model),
    ]
