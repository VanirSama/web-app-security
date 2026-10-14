import uvicorn

from src.config import DevConfig


dev_cfg = DevConfig()

if __name__ == "__main__":
    uvicorn.run("src.asgi:application", host=dev_cfg.host, port=dev_cfg.port, headers=[("server", "Malachite")],
                log_level="info", reload=True)