from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from sample.handlers import grpc_handlers as matches_grpc_handlers

# GRPC Handlers
def grpc_handlers(server):
    matches_grpc_handlers(server)