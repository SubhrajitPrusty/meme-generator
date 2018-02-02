import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


if len(sys.argv) < 2:
	print("No arguments detected. Exiting.")
else:
	memetext = sys.argv[1]
	img = sys.argv[2]

	mainImg = Image.open(img)
	width = mainImg.width
	height = mainImg.height

	imText = Image.new('RGB', (width,int(height*0.15)), (255,255,255))
	draw = ImageDraw.Draw(imText)

	font = ImageFont.truetype("Verdana.ttf",int(height*0.1))

	draw.text((20,int(imText.height*0.05)), memetext ,(0,0,0),font)

	total_h = height + imText.height

	new_im = Image.new('RGB',(width,total_h),(255,255,255))

	new_im.paste(imText, (0,0))
	new_im.paste(mainImg, (0,int(height*0.15)))

	new_im.save("meme.jpg")