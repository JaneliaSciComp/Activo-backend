from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

description = """
Activo for Active learning  
"""

# ## Items
#
# You can **read items**.
#
# ## Users
#
# You will be able to:
#
# * **Create users** (_not implemented_).
# * **Read users** (_not implemented_).


def App():
    app = FastAPI(title="Activo",
                  description=description,
                  version="0.0.1",
                  terms_of_service="http://example.com/terms/",
                  # contact={
                  #     "name": "Marwan Zouinkhi",
                  #     "url": "https://github.com/mzouink",
                  #     "email": "zouinkhi.marwan@gmail.com",
                  # },
                  license_info={
                      "name": "Apache 2.0",
                      "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                  },
                  docs_url="/")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/deploy/{path:path}")
    async def deploy_data(path: str):
        print("path: " + path)
        return {"status": "success"}

    @app.get("/data/{path:path}")
    async def get_data(path: str):
        print("path: " + path)
        return {"status": "success"}

    @app.get("/data/lazy/{path:path}")
    async def get_lazy_prediction_data(path: str):
        print("path: " + path)
        return {"status": "success"}

    @app.post("/data/annotation/{path:path}")
    async def post_annotation_data(path: str):
        print("path: " + path)
        return {"status": "success"}

    # @app.get("/")
    # async def root():
    #     return {"message": "Hello World"}

    @app.get("/data/")
    async def root():
        return {"message": "Hello World"}

    return app


def start():
    app = App()
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
