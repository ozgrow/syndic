# -*- coding: utf-8 -*-
'''
Printmodel django module for condominium

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2026 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from diacamma.condominium.models import Assembly

name = _("draft agenda")
kind = 2
modelname = Assembly.get_long_name()
value = """
<model hmargin="10.0" vmargin="10.0" page_width="210.0" page_height="297.0">
<header extent="25.0">
<text height="10.0" width="120.0" top="0.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="20" font_family="sans-serif" font_weight="" font_size="20">
{[b]}#OUR_DETAIL.name{[/b]}
</text>
<text height="10.0" width="120.0" top="10.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">
{[italic]}
#OUR_DETAIL.address - #OUR_DETAIL.postal_code #OUR_DETAIL.city - #OUR_DETAIL.tel1 #OUR_DETAIL.tel2 #OUR_DETAIL.email{[br/]}#OUR_DETAIL.identify_number
{[/italic]}
</text>
<image height="25.0" width="30.0" top="0.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">
#OUR_DETAIL.image
</image>
</header>
<bottom extent="10.0">
</bottom>
<body>
<text height="10.0" width="190.0" top="0.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="15" font_family="sans-serif" font_weight="" font_size="15">
{[b]}%(title)s{[/b]}
</text>
<text height="15.0" width="190.0" top="12.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(type)s :{[/b]} #type_assembly{[br/]}
{[b]}%(date)s :{[/b]} #date #hour{[br/]}
{[b]}%(place)s :{[/b]} #place
</text>
<table height="20.0" width="190.0" top="35.0" left="0.0" padding="1.0" spacing="0.1" border_color="black" border_style="" border_width="0.2">
    <columns width="12.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(num)s{[/b]}
    </columns>
    <columns width="128.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(item)s{[/b]}
    </columns>
    <columns width="50.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(majority)s{[/b]}
    </columns>
    <rows data="agendaitem_set">
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="9" font_family="sans-serif" font_weight="" font_size="9">
#num
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="9" font_family="sans-serif" font_weight="" font_size="9">
{[b]}#title{[/b]}{[br/]}#text
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">
#kind{[br/]}#majority
        </cell>
    </rows>
</table>
</body>
</model>""" % {'title': _('Draft agenda of the general assembly'), 'type': _('type of assembly'), 'date': _('date'), 'place': _('place'),
               'num': _('N°'), 'item': _('agenda item'), 'majority': _('majority')}
mode = 0
