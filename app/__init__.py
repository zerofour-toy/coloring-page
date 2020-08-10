import io
from fastapi import FastAPI, Request, Response, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
from PIL import Image
import numpy as np
from .image import ImageConverter

api = FastAPI(
	title="Coloring Page"
)

api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
image_converter = ImageConverter([8, 10, 12, 14])


@api.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@api.post("/api/images")
async def api_images(file: bytes = File(...)):
	upload_image = np.array(Image.open(io.BytesIO(file)))
	image = image_converter.edged_images(upload_image)
	success, encoded_image = cv2.imencode('.jpg', image)
	return Response(content=encoded_image.tobytes(), media_type='image/jpg')


@api.get("/health")
async def hello():
	return {"status": 'active'}
