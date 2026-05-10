from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_regenerate_short_codes'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE account_profile DROP COLUMN IF EXISTS checkin_token;",
            reverse_sql=migrations.RunSQL.noop,
            state_operations=[
                migrations.RemoveField(
                    model_name='profile',
                    name='checkin_token',
                ),
            ],
        ),
    ]
