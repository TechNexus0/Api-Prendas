from typing import Optional, Annotated, Any
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, PlainSerializer, WithJsonSchema

def parse_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    return str(v)

PyObjectId = Annotated[
    str,
    BeforeValidator(parse_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string", "example": "650f1f1f1f1f1f1f1f1f1f1f"})
]

class PrendaBase(BaseModel):
    prenda: str = Field(..., description="Nombre o tipo de prenda")
    talla_color: str = Field(..., description="Talla y color")
    precio_venta: float = Field(..., gt=0, description="Precio de venta")
    en_bodega: int = Field(..., ge=0, description="Cantidad en bodega")

class PrendaCreate(PrendaBase):
    pass

class PrendaUpdate(BaseModel):
    prenda: Optional[str] = None
    talla_color: Optional[str] = None
    precio_venta: Optional[float] = Field(None, gt=0)
    en_bodega: Optional[int] = Field(None, ge=0)

class PrendaResponse(PrendaBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )