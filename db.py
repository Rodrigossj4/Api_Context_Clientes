import psycopg2

# conn = psycopg2.connect(database="clientes",
#                        user="postgres",
#                        password="123456",
#                        host="bd_postgres_clientes")

conn = psycopg2.connect(database="clientes",
                        user="postgres",
                        password="123456",
                        host="localhost", port="5432")
