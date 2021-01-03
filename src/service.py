import time
import multiprocessing

import requests


class Service:
    def __init__(self, url):
        self.url = url

    def __call__(self, path):
        data = open(path, 'rb')
        response = requests.post(self.url, data=data)
        return response


class MultiProcessingService:
    def __init__(self):
        url_classification = 'http://localhost:8080/predictions/densenet161_gpu'
        url_detection = 'http://localhost:8080/predictions/fastrcnn_gpu'

        self.path_classification = '../serve/examples/image_classifier/kitten.jpg'
        self.path_detection = '../serve/examples/object_detector/persons.jpg'

        self.service_classification = Service(url_classification)
        # self.service_detection = Service(url_detection)

    def __call__(self, args):
        start = time.time()
        self.service_classification(self.path_classification)
        # self.service_detection(self.path_detection)
        end = time.time()
        print(end - start)


def single_process():
    url_classification = 'http://localhost:8080/predictions/densenet161'
    url_detection = 'http://localhost:8080/predictions/fastrcnn'

    path_classification = '../serve/examples/image_classifier/kitten.jpg'
    path_detection = '../serve/examples/object_detector/persons.jpg'

    service_classification = Service(url_classification)
    # service_detection = Service(url_detection)

    start = time.time()
    for i in range(10):
        service_classification(path_classification)
        # service_detection(path_detection)
        end = time.time()
        print(end - start)
        start = end


def multi_process():
    path_classification = '../serve/examples/image_classifier/kitten.jpg'
    path_detection = '../serve/examples/object_detector/persons.jpg'
    service = MultiProcessingService()
    with multiprocessing.Pool(2) as p:
        p.map(service, range(10))



def main(multi=False):
    if multi is False:
        start = time.time()
        single_process()
        end = time.time()
    else:
        url = 'http://localhost:8081/models'
        params_class = (
            ('url', 'densenet161.mar'),
            ('model_name', 'densenet161_gpu'),
            ('batch_size', '16'),
            ('max_batch_delay', '200'),
        )

        params_det = (
            ('url', 'fastrcnn.mar'),
            ('model_name', 'fastrcnn_gpu'),
            ('batch_size', '16'),
            ('max_batch_delay', '200'),
        )

        response = requests.post('http://localhost:8081/models', params=params_class)
        print(response)


        # response = requests.post('http://localhost:8081/models', params=params_det)
        # print(response)

        start = time.time()
        multi_process()
        end = time.time()

    print("Final time", end - start)


if __name__ == '__main__':
    main(True)

