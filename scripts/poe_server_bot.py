"""POE sever bot application"""
from typing import AsyncIterable

import fastapi_poe as fpoe
from modal import Image, Stub, asgi_app


class PoeBot(fpoe.PoeBot):
    async def get_response(
        self, request: fpoe.QueryRequest
    ) -> AsyncIterable[fpoe.PartialResponse]:
        last_message = request.query[-1].content
        yield fpoe.PartialResponse(text=last_message)

stub = Stub("poe-bot")
image = Image.debian_slim().pip_install(*REQUIREMENTS)

@stub.function(image=image)
@asgi_app()
def fastapi_app():
    bot = PoeBot()
    app = fpoe.make_app(bot, allow_without_key=True)
    return app