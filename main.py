from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/api/v1/libros/buscar")
def buscar_en_google(q: str):
    # Añadimos &langRestrict=es para que Google filtre por nosotros
    url = f"https://www.googleapis.com/books/v1/volumes?q={q}&langRestrict=es&maxResults=20"
    
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return {"error": "Error al conectar con Google Books"}
    
    libros_limpios = []
    
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        
        # Filtro extra: solo si el idioma detectado es español ('es')
        if info.get("language") == "es":
            # Verificamos que tenga título y autores antes de añadirlo
            if "title" in info and "authors" in info:
                libro = {
                    "googleId": item.get("id"),
                    "titulo": info.get("title"),
                    "autores": info.get("authors"),
                    "anio": info.get("publishedDate", "0000")[:4],
                    "portada": info.get("imageLinks", {}).get("thumbnail"),
                    "isStored": False
                }
                libros_limpios.append(libro)
            
    return libros_limpios