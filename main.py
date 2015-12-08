from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
import stipple
from connect import connect
import subprocess


def import_image_file_and_convert(filename):
    image = Image.open(filename)
    image2 = image.convert('L')
    image2.show()
    return image2


if __name__ == '__main__':
    filename = input('Please input filename: ') #get input image name
    image = import_image_file_and_convert(filename) 
    stippled = stipple.stipple(image) #.stipple use .get_initial_generators
#    print(len(stippled))
    
    
    
    im2 = Image.new('RGB', (image.size[0], image.size[1]), (255, 255, 255))
    draw2 = ImageDraw.Draw(im2)
    
    for point in stippled:
    	draw2.point((point[0], point[1]),fill = 'black')
		
    im2.save('stippled.jpg')
    
    
    connected = connect(image,stippled)
    draw = ImageDraw.Draw(connected)
    
    connected.save('connected.jpg')