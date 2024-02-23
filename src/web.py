from fastapi import FastAPI
from fastapi.responses import (
    Response,
    FileResponse,
)

from . import util

app = FastAPI()


@app.get("/favicon.ico")
async def get_favicon() -> Response:
    return Response(status_code=404)


@app.get("/{path:path}")
async def get_index(path: str) -> Response:
    record = util.get_record(path)
    if not record or not record[2]:
        if record and not record[2]:
            util.update_record(path)
        image = util.create_image()
        return Response(content=image, media_type="image/png")

    return FileResponse("src/static/image.png", media_type="image/png")
