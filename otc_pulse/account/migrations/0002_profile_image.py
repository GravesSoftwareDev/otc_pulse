from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # If 0001_initial was recorded in django_migrations but the table was
            # subsequently dropped, recreate it before adding the image column.
            sql="""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                          AND table_name   = 'account_profile'
                    ) THEN
                        CREATE TABLE account_profile (
                            id         bigserial    PRIMARY KEY,
                            otc_email  varchar(254) UNIQUE NOT NULL,
                            points     integer      NOT NULL DEFAULT 0,
                            role       varchar(10)  NOT NULL DEFAULT 'STUDENT',
                            user_id    integer      UNIQUE NOT NULL
                                           REFERENCES auth_user(id) ON DELETE CASCADE
                        );
                    END IF;
                END
                $$;
                ALTER TABLE account_profile
                    ADD COLUMN IF NOT EXISTS image varchar(100) NULL;
            """,
            reverse_sql="ALTER TABLE account_profile DROP COLUMN IF EXISTS image;",
            state_operations=[
                migrations.AddField(
                    model_name='profile',
                    name='image',
                    field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
                ),
            ],
        ),
    ]
