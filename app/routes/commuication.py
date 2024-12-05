from fastapi import WebSocket, WebSocketDisconnect, Request, APIRouter
from fastapi.responses import HTMLResponse
from app.core.websocket import manager
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates/room")
router = APIRouter()


@router.get("/communication")
async def get(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await manager.broadcast(f"User {client_id} has joined the chat!")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {client_id} has left the chat.")
