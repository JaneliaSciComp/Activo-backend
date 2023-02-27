import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import data, predictor

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


def start():
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
    app.include_router(data.router)
    app.include_router(predictor.router)

    return uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
