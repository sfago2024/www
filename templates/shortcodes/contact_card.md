<div class="contact-card" id="{{ name | slugify }}">
<a class="anchor" href="#{{ name | slugify }}">{% include "shortcodes/icon_link.html" %}</a>
<strong>{{ name }}</strong>{% if position %} — {{ position }}{% endif %}<br>
{{ body }}
</div>