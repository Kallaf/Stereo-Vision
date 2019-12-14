from PIL import Image 

images_folder = "Images/Example1"

left_img = Image.open(images_folder+'/left.png') 
right_img = Image.open(images_folder+'/right.png')  

left_img.show()
right_img.show()