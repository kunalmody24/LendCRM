# Convert pdf to image and save the image
    # images = pdf2image.convert_from_path("maybe.pdf")
    # images[0].save("maybe.jpg")
    # Load the image
    path = "Loans.pdf"
    # Get ALL tables from PDF as pandas dataframes
    dfs = tabula.read_pdf(path, multiple_tables=True)
    # img = cv2.imread('maybe.jpg')
    # Copy the image
    # cImage = np.copy(img)
    # Grayscale the image
    # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Canny-edge detection:
    # canny = cv2.Canny(gray_image, 50, 150)
    # cv2.imshow("canny", canny)
    # cv2.waitKey(0)
    # kernel = np.ones((5, 5), np.uint8)
    # dilate = cv2.dilate(canny, kernel, iterations=1)
    # cv2.imshow("dilate", dilate)
    # cv2.waitKey(0)
    # Find all horizontal/vertical lines using HoughLineTransform
    # rho = 1
    # theta = np.pi/180
    # threshold = 60
    # minLinLength = 150
    # maxLineGap = 6
    # linesP = cv2.HoughLinesP(canny, rho, theta, threshold, None, minLinLength, maxLineGap)
    # Lists for vertical/horizontal lines
    # horizontal_lines = []
    # vertical_lines = []
    # Sort lines as horizontal/vertical using linesP
    # If x1 == x2, then line is vertical, x1 is xbeginning of line and x2 is xend of line
    # If y1 == y2, then line is horizontal, y1 is ybeginning of line and y2 is yend of line
    # if linesP is not None:
    #     for i in range(0, len(linesP)):
    #         l = linesP[i][0]
    #         if (is_vertical(l)):
    #             vertical_lines.append(l)
                
    #         elif (is_horizontal(l)):
    #             horizontal_lines.append(l)
    
    # Get rid of duplicate lines with overlap filter
    # horizontal_lines = overlapping_filter(horizontal_lines, 1)
    # vertical_lines = overlapping_filter(vertical_lines, 0)
    
    # Decorate the image with lines detected (green for horizontal lines detected
    # and blue for vertical lines detected)
    # for line in horizontal_lines:
    #     cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv2.LINE_AA)
        
    # for line in vertical_lines:
    #     cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (255,0,0), 3, cv2.LINE_AA)
        
    # cv2.imshow("with_line", cImage)
    # cv2.waitKey(0)
    
    
    # ROI (Region of Interest) Selection
    # createRates(len(vertical_lines) - 2, rates)
    # Switch for determining if the next row will define the buckets for levels
    # levelsSwitch = False
    # next two variables iterate through rows
    # first_line_index = 0
    # last_line_index = len(horizontal_lines) - 1
    # thresh, bw = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)
    # for i in range(first_line_index, last_line_index):
    #     row = []
    #     # j is for iterating through columns
    #     for j in range(0, len(vertical_lines) - 1):
    #         # Identify which lines border the cell
    #         left_line_index = j
    #         right_line_index = j+1
    #         top_line_index = i
    #         bottom_line_index = i+1
    #         # Find ROI
    #         cropped_image = get_ROI(bw, horizontal_lines, vertical_lines, left_line_index,
    #                      right_line_index, top_line_index, bottom_line_index)
    #         # Detect text in the ROI
    #         text = detect(cropped_image)
    #         # Add the text to the row array
    #         row.append(text)
    #     # If findLevels is true and we haven't seen the levels row yet, then
    #     # the next row is the levels row
    #     if levelsSwitch and len(levels) == 0:
    #         createLevels(row, levels)
    #         # Turn the switch off
    #         levelsSwitch = False
    #     # Check to see if the next row will define the levels (no reason to
    #     # check next row if we have already seen it)
    #     elif not levelsSwitch and len(levels) == 0:
    #         levelsSwitch = findLevels(row)
    #     else:
    #         # Here, we are dealing with a max simultaneous/ltc/ltv row
    #         # Let's find out
    #         # Convert to lowercase
    #         row[0] = row[0].lower()
    #         if 'ltc' in row[0]:
    #             # Add an entry to the ltc dictionary
    #             ltcRow(row, ltc)
    #             # Add a column to the rates array
    #             ratesColumn(row, rates)
    #         # Is this the ltv row?
    #         elif 'ltv' in row[0]:
    #             # Call function to populate the ltv dictionary
    #             createltv(row, ltv, levels)
    #     print(row)
    # housesFlipped = (int) (input("Enter houses flipped:"))
    # ltcVal = (float) (input("Enter an LTC VALUE"))
    # index1 = ltc[ltcVal]
    # index2 = levels[housesFlipped]
    # print("Interest rate: " + str(rates[index1][index2]))
    # print("LTV Value: " + str(ltv[housesFlipped]))
    
    
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

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[y:y+h, x:x+w]
    return cropped_image

def get_ROI(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset
    
    w = x2 - x1
    h = y2 - y1
    
    cropped_image = get_cropped_image(image, x1, y1, w, h)
    
    return cropped_image

def detect(cropped_frame, is_number = False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame)
    else:
        text = pytesseract.image_to_string(cropped_frame)
    return text