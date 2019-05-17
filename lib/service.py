"""Service layer module
"""
from concurrent import futures
import grpc
from io import BytesIO
import logging
from PIL import Image
import sys
import time

import config_pb2, config_pb2_grpc
from img_to_vec import Img2Vec

CHUNK_SIZE = 1024 * 1024  # 1MB
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def read_image_file_in_chunks(files):
    """Read image files in chucks
        Args:
            files: (list) List of first and second image file locations
        Returns:
            Generator object of the image bytes
    """
    for file_index, filename in enumerate(files):
        with open(str(filename), 'rb') as f:
            while True:
                piece = f.read(CHUNK_SIZE)
                if len(piece) == 0:
                    break
                yield config_pb2.ImageBuffer(buffer=piece, fileindex=file_index)


def read_image_bytes_on_server(chunks):
    """Read image buffer bytes on server
        Args:
            chunks: Generator object of the image files
        Returns:
            Generator of the image file name and full stream of image
    """
    img_data = {}
    for chunk in chunks:
        stream = img_data.get(chunk.fileindex, BytesIO())
        stream.write(chunk.buffer)
        img_data[chunk.fileindex] = stream
    return img_data.values()


class MLClient(object):
    """MLClient entry service
    """
    def __init__(self, address):
        # Connect to the gRPC server
        channel = grpc.insecure_channel(address)
        # Get gRPC server stub
        self.stub = config_pb2_grpc.MLServerStub(channel)

    def image_similarity(self, first_image, second_image):
        """Function to find similarity between two images
            Args:
                first_image: (Path) first image file location for comparision
                second_image: (Path) second image file location for comparision
            Returns:
                None
        """
        # Create a stream for image files
        image_chunks_generator = read_image_file_in_chunks([first_image, second_image])
        # Call service from the Server to find similarity between images
        return self.stub.image_similarity(image_chunks_generator)


class MLServicer(config_pb2_grpc.MLServerServicer):
    """ML servicer for the gRPC server
    """

    def image_similarity(self, request_iterator, context):
        """Find image similarity between two images
        """
        # Initialize ML library to compare similarity between images
        img_vec = Img2Vec()

        # Read image stream in chunks received from client end
        image_streams = read_image_bytes_on_server(request_iterator)

        vectors = []
        for image_bytes in image_streams:
            # Create PIL image object from the image stream
            pil_image = Image.open(image_bytes)
            # Convert PIL image object into vectors
            vectors.append(img_vec.get_vec(pil_image, tensor=True))
            # Close image bytes streaming
            image_bytes.close()

        assert len(vectors) == 2  # Must be two vectors as we are comparing to images, one for each
        # Find out similarity between images
        similarity = img_vec.cosine_similarity(*vectors)
        # Send response to the client
        return config_pb2.Reply(similarity=similarity)


class MLServer(config_pb2_grpc.MLServerServicer):
    def __init__(self):
        # Create server pool
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # Bind servicer object to the gRPC server
        config_pb2_grpc.add_MLServerServicer_to_server(MLServicer(), self.server)

    def start(self, port):
        """Start ML server
            Args:
                port: (int) port number to run ML server
            Returns:
                None
        """
        # Logging configurations
        logging.basicConfig(stream=sys.stdout, format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)
        # Assign port to the gRPC server
        self.server.add_insecure_port(f'[::]:{port}')
        # Start gRPC server
        self.server.start()
        logging.info("ML server listening at port {}. Press CTRL+C to stop".format(port))
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.server.stop(0)
