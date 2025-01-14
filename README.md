### Django Socio gRPC
[Django Socio gRPC](https://django-socio-grpc.readthedocs.io/en/latest/getting-started.html)

1. **Generate proto file for model**
You can also make proto file manualy.
```shell
python manage.py generateproto
```
2. **Generate GRPC code**
* Sample
```shell
python -m grpc_tools.protoc --proto_path=./sample --python_out=./sample --grpc_python_out=./sample ./sample/grpc/sample.proto
```

3. **Running the gRPC server**

```shell
python manage.py grpcrunaioserver --dev
```