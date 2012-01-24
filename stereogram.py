import Image
from random import randrange

def gen_strip(width, height):
    img = Image.new("RGB", (width, height))
    pix = img.load()
    for x in range(width):
        for y in range(height):
            I = 2**randrange(8)
            pix[x,y] = (I,I,I)
    return img
    
def gen_stereogram(depth, strips=8, levels=48, zoom = 1):
    strip_width = depth.size[0] // (strips - 5)
    print strip_width
    width = strip_width * strips
    height = depth.size[1]
    img = Image.new("RGB", (width, height))
    
    strip = gen_strip(strip_width, height)
    strip_pix = strip.load()

    depth = depth.convert('I')
    depth_pix = depth.load()
    img_pix = img.load()
    for y in range(img.size[1]):
        for x in range(strip_width):
            img_pix[x,y] = strip_pix[x,y]
            
        for x in range(strip_width, strip_width*3):
            img_pix[x,y] = img_pix[x-strip_width,y]
        
        for x in range(depth.size[0]):
            depth_offset = round(depth_pix[x,y] / 255.0 * levels) * zoom
            tx = x + strip_width*3
            img_pix[tx,y] = img_pix[tx-strip_width+depth_offset,y]
            
        for x in range(strip_width*3 + depth.size[0], img.size[0]):
            img_pix[x,y] = img_pix[x-strip_width,y]
            
    return img

def main():
    depth = Image.open("SampleDepthMap.gif")
    stereo = gen_stereogram(depth, strips=12, levels=64, zoom=1)
    
    stereo.show()
    
if __name__ == "__main__":
    main()