from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from sample.services import (
    MatchesService,
)
def grpc_handlers(server):
    app_registry = AppHandlerRegistry("sample", server)
    app_registry.register(MatchesService)