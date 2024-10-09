from django.contrib import admin

from iyfconnect.settings.base import ENVIRONMENT

env_mapping = {
    'local': 'Local',
    'staging': 'Dev',
    'production': 'Live'
}

env_alias = env_mapping[ENVIRONMENT]
admin.site.site_header = f"IyfConnect Backend - {env_alias}"
admin.site.site_title = f"IyfConnect Backend - {env_alias}"
admin.site.index_title = f"IyfConnect Backend Admin - {env_alias}"
