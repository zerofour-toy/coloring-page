from fastapi import FastAPI

api = FastAPI(
	title="Coloring Page"
)


@api.get("/")
def index():
	return {"hello": "word"}

