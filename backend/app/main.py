from fastapi import FastAPI
from app.api import content, auth, social, news
from app.services.scheduler import schedule_post
from app.services.lang_integration import integrate_with_lang_tools
from app.services.rag_pipeline import generate_scientific_content  # Importar la función de generación de contenido científico
from app.db.sqlite import init_db as init_sqlite_db
from app.db.mongodb import init_mongo_db
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Inicializar bases de datos
@app.on_event("startup")
async def startup_event():
    init_sqlite_db()
    init_mongo_db()

# Incluir routers
app.include_router(content.router, prefix="/content", tags=["content"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(social.router, prefix="/social", tags=["social"])
app.include_router(news.router, prefix="/news", tags=["news"])

# Endpoint de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the IngenIAtor content generation system!"}

# Endpoint para programar publicaciones
@app.post("/schedule_post")
def schedule_post_endpoint(content: str, platform: str, schedule_time: str):
    schedule_post(content, platform, schedule_time)
    return {"message": "Post scheduled successfully"}

#Endpoint integracion con ecosistema lang
@app.get("/integrate_lang-tools")
def integrate_lang_tools_endpoint(input_data: str = Query(...), language: str = Query(...), personal_info: str = Query(None)):
    result = integrate_with_lang_tools(input_data, language, personal_info)
    return result

# Endpoint para generar contenido científico
@app.post("/generate_scientific_content")
def generate_scientific_content_endpoint(request: ContentRequest):
    response = generate_scientific_content(request)
    return response
