{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
dear user : {{ email }}<br>
here is your account activation url:<br>
http://127.0.0.1/accounts/api/v1/activation/confirm/{{ token }}/
{% endblock %}