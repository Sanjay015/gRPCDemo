About
-----
A [gRPC](https://grpc.io/docs/quickstart/python/) client server architecture to find out the similarity between two image files.
A Machine Learning stack should be up and running on server and a client can make request to the server by passing
two image files to get the similarity between them. Protobuff is being use to transfer data between client and server.

Requirements
------------
Working in conda environment is recommended. You need to install below packages -
- [PyTorch](https://anaconda.org/pytorch/pytorch)
- [torchvision](https://anaconda.org/pytorch/torchvision)
- [grpcio](https://anaconda.org/conda-forge/grpcio)
- Numpy
- PIL
- Python `3.6` or `above` recommended

About protbuff schema config
----------------------------
- There is a [protobuff](https://developers.google.com/protocol-buffers/docs/overview) data configuration file available [here](proto/config.proto).
- This is being used to create data structure schema. This schema file helps you to create protobuff configuration in python.
- [config_pb2.py](lib/config_pb2.py) and [config_pb2_grpc.py](lib/config_pb2_grpc.py) are created by using [here](proto/config.proto)
schema file.
- You need to run [setup.py](setup.py) to generate protobuff python config.

How to Use
----------
- Clone this repository
- Run `python setup.py` to generate python files based on protobuff schema
- Navigate to `lib` and run `python server.py --port=8080(default 9988)`
- In a new window, Navigate to `lib` and run `python client.py` + command line arguments-
  - Command line arguments for `client.py`
    - `--port` (default `9988`) port number on which server is running(which you started in step 3)
    - `--host` (default `localhost`) host on which gRPC server is running
    - `--first_image` Location of first image file
    - `--second_image` Location of second image
  - Example
    ```
    python client.py --host=localhost --port=9988 --first_image=/temp/image1.jpg --second_image=/temp/image2.jpg
    ```
