from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_DETAILS = config("MONGODB_URL", default="mongodb://localhost:27017")
DATABASE_NAME = config("DATABASE_NAME", default="prendas_db")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[DATABASE_NAME]

collection_prendas = database.get_collection("prendas_vestir")

async def verificar_conexion():
    try:
        await client.admin.command('ping')
        print(f"¡Conexión exitosa a la base de datos '{DATABASE_NAME}'")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")