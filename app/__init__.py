from fastapi import FastAPI, Request, Response, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .image import ImageConverter
from . import util

api = FastAPI(
	title="Coloring Page"
)

api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
image_converter = ImageConverter([8, 10, 12, 14])


@api.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@api.get("/test", response_class=HTMLResponse)
async def test(request: Request):
	return templates.TemplateResponse("test.html", {"request": request})


@api.post("/api/images")
async def api_images(file: UploadFile = File(...)):
	orig_content = await file.read()
	orig_image = util.create_image(orig_content)
	convert_images = image_converter.edged_images(orig_image)

	origin = util.meta_raw_image(orig_content, file.filename, file.content_type)
	converts = []
	for convert_image in convert_images:
		converts.append(util.meta_image(convert_image, "cvt.jpg", "image/jpeg"))

	return {
		"origin": origin,
		"converts": converts
	}


@api.get("/health")
async def hello():
	return {"status": 'active'}


