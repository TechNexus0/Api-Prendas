from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from database import collection_prendas, verificar_conexion
from models import PrendaCreate, PrendaUpdate, PrendaResponse

app = FastAPI(
    title="API Tienda de Ropa - ADSO",
    description="API RESTful asíncrona con FastAPI, Motor y MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await verificar_conexion()

@app.post("/prendas/", response_description="Crear una nueva prenda", response_model=PrendaResponse, status_code=status.HTTP_201_CREATED)
async def crear_prenda(prenda: PrendaCreate):
    prenda_dict = prenda.model_dump()
    nueva_prenda = await collection_prendas.insert_one(prenda_dict)
    prenda_creada = await collection_prendas.find_one({"_id": nueva_prenda.inserted_id})
    return prenda_creada

@app.get("/prendas/", response_description="Listar todas las prendas", response_model=list[PrendaResponse])
async def obtener_prendas():
    prendas = []
    async for prenda in collection_prendas.find():
        prendas.append(prenda)
    return prendas

@app.get("/prendas/{id}", response_description="Obtener una prenda por ID", response_model=PrendaResponse)
async def obtener_prenda(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido.")
    
    prenda = await collection_prendas.find_one({"_id": ObjectId(id)})
    if prenda is None:
        raise HTTPException(status_code=404, detail=f"Prenda con ID {id} no encontrada.")
    return prenda

@app.put("/prendas/{id}", response_description="Actualizar una prenda", response_model=PrendaResponse)
async def actualizar_prenda(id: str, prenda_in: PrendaUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido.")
    
    datos_actualizar = {k: v for k, v in prenda_in.model_dump(exclude_unset=True).items()}
    
    if len(datos_actualizar) > 0:
        resultado = await collection_prendas.update_one(
            {"_id": ObjectId(id)}, {"$set": datos_actualizar}
        )
        if resultado.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Prenda con ID {id} no encontrada.")
            
    prenda_actualizada = await collection_prendas.find_one({"_id": ObjectId(id)})
    return prenda_actualizada

@app.delete("/prendas/{id}", response_description="Eliminar una prenda", status_code=status.HTTP_200_OK)
async def eliminar_prenda(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="El ID proporcionado no es válido.")
        
    resultado = await collection_prendas.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Prenda con ID {id} no encontrada.")
        
    return {"mensaje": f"Prenda con ID {id} eliminada exitosamente."}