from ManualImageClassification.classifier_canvas import ClassifierCanvas
import os


def run():
    pics_dir = os.path.join(os.getcwd(), 'example/pictures')
    ClassifierCanvas(directory_of_images=pics_dir, categories=['tree', 'monster'])


if __name__ == "__main__":
    run()
