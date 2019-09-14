import argparse
import sys
import yaml

from PIL import Image
from yaml import Loader

def build_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="path to task file")
    return parser
        
class CropStep:
    left = 0
    top = 0
    right = 0
    bottom = 0

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        return '%s{L: %d, T:%d, R:%d,B: %d}' % (type(self).__name__,self.left, self.top, self.right, self.bottom)

class Task:

    def __init__(self,**entries):
        self.steps = []
        rawSteps = entries.pop('steps')
        self.__dict__.update(entries)
        for step in rawSteps:
            if step['type'] == 'crop':
                self.steps.append(CropStep(**step['bounds']))

    def __str__(self):
        return '%s{steps: %s}' % (type(self).__name__, ['%s' % step for step in self.steps])

if __name__ == '__main__':
    args = build_argument_parser().parse_args()
    
    if args.file is None:
        sys.exit('Task file argument not provided')

    tasks = []
    with open(args.file,"r") as f:
        data = yaml.safe_load(f)

        for task in data['tasks']:
            tasks.append(Task(**task))
    
    for task in tasks:
        
        image = Image.open(task.sourceFile)

        for step in task.steps:
            try:
                cropped = image.crop((step.left,step.top,step.right,step.bottom))
                cropped.save(task.targetFile,task.outputFormat)
            except Exception as e:
                print('Error with file %s: %s' % (task.sourceFile,e))
                continue
