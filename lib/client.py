"""gRPC client module
"""
import argparse
import logging
import os
from pathlib import Path
import sys

from service import MLClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_client(first_image: Path, second_image: Path, host: str = "localhost", port: int = 9988):
    """Run gRPC client
        Args:
            first_image: Location of first image to compare
            second_image: Location of second image to compare
            host: Host on which gRP server is running
            port: Port number on which gRPC server is running
    """
    grpc_server = "{}:{}".format(host, port)
    client = MLClient(grpc_server)
    logging.debug("Calculating similarity between images")
    response = client.image_similarity(first_image, second_image)
    logging.info("Similarity between {} and {} is: {}".format(first_image, second_image, response.similarity))


if __name__ == '__main__':
    # Default sample images to compare
    default_first_image = os.path.join(BASE_DIR, "images", "SampleCar1.jpg")
    default_second_image = os.path.join(BASE_DIR, "images", "SampleCar2.jpg")

    # Logger setup
    logging.basicConfig(stream=sys.stdout, format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)

    # Parse Command Line arguments
    parser = argparse.ArgumentParser(description="Command line argument parser")
    parser.add_argument("--host", type=str, default="localhost",
                        help="Host on which gRPC server is running, default localhost")
    parser.add_argument("--port", type=int, default=9988,
                        help="Port number on which gRPC server is running, default 9988")
    parser.add_argument("--first_image", type=str, default=default_first_image, help="First image file to compare")
    parser.add_argument("--second_image", type=str, default=default_second_image, help="Second image file to compare")

    args = parser.parse_args()

    # Get first image
    if not os.path.exists(args.first_image):
        raise FileNotFoundError("File {} does not exist".format(args.first_image))
    # Get second image
    if not os.path.exists(args.second_image):
        raise FileNotFoundError("File {} does not exist".format(args.second_image))

    run_client(args.first_image, args.second_image, host=args.host, port=args.port)
