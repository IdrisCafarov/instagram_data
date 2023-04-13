from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Truncate all tables and reset sequences in the database.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$
                DECLARE
                    tbl_name text;
                BEGIN
                    FOR tbl_name IN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public')
                    LOOP
                        EXECUTE 'TRUNCATE TABLE ' || tbl_name || ' CASCADE';
                    END LOOP;

                    -- Reset sequences
                    PERFORM setval(pg_get_serial_sequence('"' || table_name || '"', column_name), 1, false)
                    FROM information_schema.columns
                    WHERE column_default LIKE 'nextval%';
                END $$;
            """)

            self.stdout.write(self.style.SUCCESS('Database has been reset successfully.'))
