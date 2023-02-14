from PIL import Image
def processor(filename):
      file = './static/process/' + filename
      Img = Image.open(file)
      grey = Img.convert('L')
      grey.save(file)
