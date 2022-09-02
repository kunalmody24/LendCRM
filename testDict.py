import re
import cv2
import pdf2image
import numpy as np
import matplotlib.pyplot as plt
import tabula
import io
import boto3
from PIL import Image
import pandas as pd
import pytesseract
from tabulate import tabulate

def main():
    
    # dfs = tabula.read_pdf("Loans3.pdf", multiple_tables=True)
    # for i in range(len(dfs)):
    #     print(dfs[i])
    #     print('\n')
        
    # print(tabulate(dfs[2]))
    # images = pdf2image.convert_from_path("Loans.pdf")
    # images[0].save("loans.jpg")
    # # Load the image
    # img = cv2.imread('loans.jpg')
    # text = pytesseract.image_to_string(img)
    # print(text)
    # cImage = img.copy()
    # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # canny = cv2.Canny(gray_image, 50, 150)
    # cv2.imshow("canny", canny)
    # cv2.waitKey(0)
    # kernel = np.ones((5, 5), np.uint8)
    # dilate = canny
    # for i in range(2):
    #     dilate = cv2.dilate(dilate, kernel, iterations=1)
    # erode = dilate
    # cv2.imshow("dilate", dilate)
    # cv2.waitKey(0)
    # for i in range(3):
    #     erode = cv2.erode(erode, None, iterations=i+1)
    #     cv2.imshow("erode", erode)
    #     cv2.waitKey(0)
    # rho = 1
    # theta = np.pi/180
    # threshold = 110
    # minLinLength = 100
    # maxLineGap = 1
    # linesP = cv2.HoughLinesP(erode, rho, theta, threshold, None, minLinLength, maxLineGap)
    # horizontal_lines = []
    # vertical_lines = []
    # for i in range(0, len(linesP)):
    #     l = linesP[i][0]
    #     if (is_vertical(l)):
    #         vertical_lines.append(l)
            
    #     elif (is_horizontal(l)):
    #         horizontal_lines.append(l)
    # # horizontal_lines = overlapping_filter(horizontal_lines, 1)
    # # vertical_lines = overlapping_filter(vertical_lines, 0)
    # for line in horizontal_lines:
    #     cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv2.LINE_AA)
        
    # for line in vertical_lines:
    #     cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (255,0,0), 3, cv2.LINE_AA)
        
    # cv2.imshow("with_line", cImage)
    # cv2.waitKey(0)
    return

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']

def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }

def is_vertical(line):
    delta = 1/1000
    return abs(line[0] - line[2]) < delta

def is_horizontal(line):
    delta = 1/1000
    return abs(line[1] - line[3]) < delta

def overlapping_filter(lines, sorting_index):
    filtered_lines = []
    lines = sorted(lines, key=lambda line: line[sorting_index])
    separation = 10
    for i in range(len(lines)):
            l_curr = lines[i]
            if(i > 0):
                l_prev = lines[i - 1]
                if ( (l_curr[sorting_index] - l_prev[sorting_index]) > separation):
                    filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)
                
    return filtered_lines



if __name__ == "__main__":
    main()