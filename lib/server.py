"""gRPC server module
"""
import argparse
from service import MLServer

if __name__ == '__main__':
    # Command Line Argument parser
    parser = argparse.ArgumentParser(description="Command line argument parser")
    parser.add_argument("--port", type=int, default=9988, help="Port number to start gRPC server, default 9988")
    args = parser.parse_args()
    ml_server = MLServer()
    ml_server.start(args.port)
