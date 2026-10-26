from django.db import migrations
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import Parameter


def theme_parameter(*_args):
    set_locale_lang(settings.LANGUAGE_CODE)
    Parameter.check_and_create(name='syndic-theme', typeparam=Parameter.TYPE_SELECT, title=_("syndic-theme"),
                               args="{'Enum':2}", value=0, param_titles=(_("syndic-theme.0"), _("syndic-theme.1")))


class Migration(migrations.Migration):

    dependencies = [
        ('syndic', '0002_check_journal'),
        ('CORE', '0007_shortcut'),
    ]

    operations = [
        migrations.RunPython(theme_parameter),
    ]
