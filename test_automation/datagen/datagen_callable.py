from test_automation.datagen.datagen_service.datagen_service import DataGenService


class DataGen:
    def __init__(self):
        self.value = ''

    def __call__(self, name: str):
        self.value = DataGenService().getValueByName(name)
        return self.value


class DataGenContext:
    def __enter__(self):
        self.datagen = DataGen()
        return self.datagen

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# TODO: create other types of data generators: file based, Fake library ...
