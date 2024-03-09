from fastapi import FastAPI
from fastapi.responses import (
    FileResponse,
    Response,
)

from . import util

app = FastAPI()


@app.get("/{path:path}")
async def get_index(path: str) -> Response:
    try:
        record = util.get_record(path)
        if not record:
            raise ValueError("Unknown uuid")
    except ValueError:
        return Response(status_code=404)

    uid = util.parse_uuid(path)
    if not record[-1]:
        if uid.version() == 3:
            return Response(status_code=404)
        util.update_record(path)

    if uid.version() == 4:
        image = util.create_image()
        return Response(content=image, media_type="image/png")
    return FileResponse("src/static/image.png", media_type="image/png")
