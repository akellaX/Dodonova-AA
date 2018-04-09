from PIL import Image

image = Image.open("C:\\Users\\User\\Desktop\\car_proj\\back_view.png").convert('RGBA')
alpha = image.split()[-1]
bg = Image.new("RGBA", image.size, (0,0,0,255))
bg.paste(alpha, mask=alpha)
bg.convert('L').convert('P', palette=Image.ADAPTIVE, colors=8).save("C:\\Users\\User\\Desktop\\123.png",optimize=True)