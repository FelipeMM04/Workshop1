import sqlalchemy as sa

# Reemplaza 'TU_CONTRASEÑA' con la clave que usas en MySQL Workbench
DB_USER = "root"
DB_PASS = "ADsemestre2025" 
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "kimball_dw"

# Crear la URL de conexión
connection_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = sa.create_engine(connection_url)
    with engine.connect() as conn:
        print("¡Conexión exitosa a MySQL y a la base de datos kimball_dw!")
except Exception as e:
    print("Error al conectar a la base de datos:")
    print(e)