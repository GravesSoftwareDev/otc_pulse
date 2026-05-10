import uuid
import random
import string
from django.db import migrations, models


def assign_tokens(apps, schema_editor):
    Profile = apps.get_model('account', 'Profile')
    for profile in Profile.objects.filter(checkin_token=None):
        profile.checkin_token = uuid.uuid4()
        profile.save(update_fields=['checkin_token'])


def populate_short_codes(apps, schema_editor):
    chars = string.ascii_uppercase + string.digits
    Profile = apps.get_model('account', 'Profile')
    used = set(Profile.objects.exclude(short_code='').values_list('short_code', flat=True))
    for profile in Profile.objects.filter(short_code=''):
        code = ''.join(random.choices(chars, k=8))
        while code in used:
            code = ''.join(random.choices(chars, k=8))
        used.add(code)
        profile.short_code = code
        profile.save(update_fields=['short_code'])


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_image'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE account_profile ADD COLUMN IF NOT EXISTS checkin_token uuid NULL;",
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AddField(
                    model_name='profile',
                    name='checkin_token',
                    field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
                ),
            ],
        ),
        migrations.RunPython(assign_tokens, migrations.RunPython.noop),
        migrations.RunSQL(
            sql="""
                ALTER TABLE account_profile ALTER COLUMN checkin_token SET NOT NULL;
                DO $$ BEGIN
                    ALTER TABLE account_profile
                        ADD CONSTRAINT account_profile_checkin_token_key UNIQUE (checkin_token);
                EXCEPTION WHEN duplicate_object THEN NULL;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AlterField(
                    model_name='profile',
                    name='checkin_token',
                    field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
            ],
        ),
        migrations.RunSQL(
            sql="ALTER TABLE account_profile ADD COLUMN IF NOT EXISTS short_code varchar(8) NOT NULL DEFAULT '';",
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AddField(
                    model_name='profile',
                    name='short_code',
                    field=models.CharField(blank=True, default='', max_length=8),
                    preserve_default=False,
                ),
            ],
        ),
        migrations.RunPython(populate_short_codes, migrations.RunPython.noop),
        migrations.RunSQL(
            sql="""
                DO $$ BEGIN
                    ALTER TABLE account_profile
                        ADD CONSTRAINT account_profile_short_code_key UNIQUE (short_code);
                EXCEPTION WHEN duplicate_object THEN NULL;
                END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.AlterField(
                    model_name='profile',
                    name='short_code',
                    field=models.CharField(blank=True, max_length=8, unique=True),
                ),
            ],
        ),
    ]
