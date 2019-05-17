"""Module to convert protobuf files to .py files
"""
import os
from grpc_tools import protoc

# Project's root location
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Protobuff configurations root location
proto_path = os.path.join(ROOT_PATH, "proto")

# Python and gRPC output location
out_path = os.path.join(ROOT_PATH, "lib")

# Create output directory if not exists
if not os.path.exists(out_path):
    os.makedirs(out_path, exist_ok=True)

# Protobuff config file location
proto_file = os.path.join(ROOT_PATH, "proto", "config.proto")

# Generate python and gRPC files
protoc.main(
    (
        '-I.',
        '--proto_path={}'.format(proto_path),
        '--python_out={}'.format(out_path),
        '--grpc_python_out={}'.format(out_path), '{}'.format(proto_file)
    )
)
