from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import click
import time

def memegen(mainImg, text):
	words = text.split(" ") # extract words
	wordlen = [len(x) for x in words] # extract length of each words

	width = mainImg.width
	height = mainImg.height
	
	fontsize = int(height*0.05) # looks good enough
	font = ImageFont.truetype(os.path.join("fonts","impact.ttf"), fontsize) # select font
	fwidth, fheight = font.getsize("W") # W is the widest letter in the english alphabet

	# do check https://stackoverflow.com/questions/3949422/which-letter-of-the-english-alphabet-takes-up-most-pixels#3949453
	
	# print(fwidth, fheight)
	maxletters = (width//fwidth)*2 # adjustment because font size is weird

	lines = []
	i = k = 0
	while i < len(words): # divide text into lines that can fit
		line = []
		s = 0
		while k < len(words):
			s+=len(words[k])
			s+=1
			if s < maxletters:
				line.append(words[k])
			else:
				break
			k+=1
		lines.append(" ".join(line))
		i=k

	# print(lines)
	# print([len(x) for x in lines])
	# print(height, width, fontsize, maxletters)

	lineheight = 1.5
	textHeight = int((fontsize*lineheight)*len(lines)) # get total height of text

	imText = Image.new('RGB', (width, textHeight), (255,255,255)) # make image space for text
	draw = ImageDraw.Draw(imText)

	memetext = "\n".join(lines)
	draw.text((fontsize//3, fontsize//3), memetext, (0,0,0), font)

	total_h = height + imText.height # total height of text + image

	new_im = Image.new('RGB',(width,total_h),(255,255,255)) # make new image with size of text space + old image

	new_im.paste(imText, (0,0)) # paste text at top
	new_im.paste(mainImg, (0,textHeight)) # paste image below text

	return new_im

@click.command()
@click.argument("image", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("text", type=click.STRING)
@click.option("--show", is_flag=True, help="open the image in a image viewer")
def cli(image, text, show):
	""" Generate a text + image meme """
	img = Image.open(image)
	if img.height < 100 or img.width < 100:
		img = img.resize((img.width*4, img.height*4))
	elif img.height < 200 or img.width < 200:
		img = img.resize((img.width*2, img.height*2))
	img = memegen(img, text)

	if show:
		img.show()
	
	img.save("meme-{}.jpg".format(int(time.time())))

