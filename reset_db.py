from database.connection import reset_database

reset_database()
print("Database reset: tables rebuilt from schema.sql and sample data loaded from seed.sql.")
