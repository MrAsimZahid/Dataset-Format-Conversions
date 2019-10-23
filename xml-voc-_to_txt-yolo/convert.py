import os
import sys
from xml.dom import minidom
from decimal import Decimal as dec

NUMBER_OF_DIGITS_TO_TRUNCATE = 6

def truncate(num_list):
    for i, val in enumerate(num_list):
        num_list[i] = float(round(dec(val),NUMBER_OF_DIGITS_TO_TRUNCATE))


def generate_classes_file(classes_list,path_of_file_creation):
    txt_file = open(path_of_file_creation+"classes.txt","w+")
    for i in classes_list:
        txt_file.write(i)
        txt_file.write("\n")
    
    txt_file.close()



def handle_index_ValueError(class_name, classes_list, ob_class):
    for val in class_name:
        try:
            classes_list.index(val)
        except ValueError:
            classes_list.append(val)
        
        #print(classes_list.index(val))
        ob_class.append(classes_list.index(val))

    #print(classes_list)
    #print(class_name)
    #print(ob_class)


#this function returns the value of a given tag in list format, 
#the return format is a list even when there is only one number
def return_list_from_xml_field(xml_field):
    elements = []
    for i in xml_field:
        elements.append(i.toxml().split(">")[1].split("<")[0]) #this is ugly, i know
    return elements

def get_data_from_xml(path_to_xml_file):

    #load xml file

    xmldoc = minidom.parse(path_to_xml_file)

    #get the classes names from xml

    class_name = return_list_from_xml_field(xmldoc.getElementsByTagName('name'))

    #load images width and height from xml file

    image_width = return_list_from_xml_field(xmldoc.getElementsByTagName('width'))
    image_height = return_list_from_xml_field(xmldoc.getElementsByTagName('height'))

    image_width = list(map(float,image_width))
    image_height = list(map(float,image_height))

    #load bouding boxes width and height from xml file

    x_max = return_list_from_xml_field(xmldoc.getElementsByTagName('xmax'))
    x_min = return_list_from_xml_field(xmldoc.getElementsByTagName('xmin'))
    y_max = return_list_from_xml_field(xmldoc.getElementsByTagName('ymax'))
    y_min = return_list_from_xml_field(xmldoc.getElementsByTagName('ymin'))

    x_max = list(map(float,x_max))
    x_min = list(map(float,x_min))
    y_max = list(map(float,y_max))
    y_min = list(map(float,y_min))

    absolute_x = []
    absolute_y = []
    absolute_width = []
    absolute_height = []

    #if your xml has more than one labeled object, the x_max,x_min,y_max,y_min will be lists
    for i in range(len(x_max)):

        #calculate the bouding box center in x axis and y axis
    
        absolute_x.append(x_min[i] + 0.5 * (x_max[i] - x_min[i]))
        absolute_y.append(y_min[i] + 0.5 * (y_max[i] - y_min[i]))

        #calculate absolute width and height from bouding boxes

        absolute_width.append(x_max[i] - x_min[i])
        absolute_height.append(y_max[i] - y_min[i])

    return class_name,absolute_x,absolute_y,absolute_width,absolute_height, image_width, image_height


def transform_from_xml_to_txt_format(absolute_x,absolute_y,absolute_width,absolute_height,image_width,image_height):

    #yolo coordinates of the bouding boxes are relative to image,
    # so we have to divide the measures by the image measures 
    x = []
    y = []
    width = []
    height = []
    for i in range(len(absolute_width)):
        x.append(absolute_x[i] / image_width[0])
        y.append(absolute_y[i] / image_height[0])
        width.append(absolute_width[i] / image_width[0])
        height.append(absolute_height[i] / image_height[0])

    return x, y, width, height

def create_txt_file(ob_class,x,y,width,height,path_of_file_creation,file_name):
    #open file on writing mode, write values received and close the file
    txt_file = open(path_of_file_creation+file_name+str(.txt),"w+")

    truncate(x)
    truncate(y)
    truncate(width)
    truncate(height)

    x = list(map(str,x))
    y = list(map(str,y))
    width = list(map(str,width))
    height = list(map(str,height))
    ob_class = list(map(str,ob_class))


    for i in range(len(ob_class)):
        # print("imagem:"+str(i))
        # print(x[i])
        # print(y[i])
        # print(width[i])
        # print(height[i])
        txt_file.write(ob_class[i]+" "+x[i]+" "+y[i]+" "+width[i]+" "+height[i])
        txt_file.write("\n")
    
    txt_file.close()


if __name__ == "__main__":
    classes_list = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".xml"):
            class_name,absolute_x,absolute_y,absolute_width,absolute_height, image_width, image_height = get_data_from_xml(sys.argv[1]+file)
            ob_class = []

            handle_index_ValueError(class_name,classes_list,ob_class)

           

            x,y,width,height = transform_from_xml_to_txt_format(absolute_x,absolute_y,absolute_width,absolute_height, image_width, image_height)
            create_txt_file(ob_class,x,y,width,height,sys.argv[2],file[:-4])

    generate_classes_file(classes_list,sys.argv[2])
    #print("Conversão efetuada com sucesso.")