from PIL import Image
import numpy
import os


image_path = "C:/Users/PC/Documents/md5/steganography/aladin.jpg"
watermarked_image_path = "C:/Users/PC/Documents/md5/steganography/watermarked_image.png"

def lsb_1(image_path, message):
	image_object = Image.open(image_path)
	image_array = numpy.array(image_object)

	image_array -= image_array % 2 # passage de tous les pixels en valeur pair

	binary_message = [int(bin_number) for bin_number in ''.join(format(ord(i), '08b') for i in message)] # convert message to binary

	number_rows, number_cols, number_color = image_array.shape
	index_binary_message = 0
	for index_row in range(0, number_rows):
		for index_col in range(0, number_cols):
			for index_color in range(0, number_color):
				if index_binary_message < len(binary_message) :
					image_array[index_row, index_col, index_color] += binary_message[index_binary_message]
				else :
					break
				index_binary_message += 1

	watermarked_image_object = Image.fromarray(image_array, "RGB")
	
	root_path = os.path.split(image_path)[0]
	watermarked_image_path = os.path.join(root_path, "watermarked_image.png")
	watermarked_image_object.show()

	watermarked_image_object.save(watermarked_image_path)



def extract_message_from_image(watermarked_image_path):
	watermarker_image_object = Image.open(watermarked_image_path)
	watermarker_image_array = numpy.array(watermarker_image_object)

	binary_message_array = watermarker_image_array % 2
	binary_message_list = []
	number_rows, number_cols, number_color = binary_message_array.shape
	for index_row in range(0, number_rows):
		for index_col in range(0, number_cols):
			for index_color in range(0, number_color):
				binary_message_list.append(str(binary_message_array[index_row, index_col, index_color]))
				if binary_message_list[-8:] == ["0"]*8:
					binary_message = "".join(binary_message_list)
					message = ''.join([chr(int(binary_message[i : i+8],2)) for i in range(0, len(binary_message), 8)])
					return message


lsb_1(image_path, "Coucou les loulous")
print(extract_message_from_image(watermarked_image_path))