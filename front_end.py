from PyQt5 import QtGui, uic ,QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
import sys
from time import strftime
from subprocess import call

import xml.etree.ElementTree as ET
import csv
import os
import xml.etree.ElementTree as ET

root = os.path.expanduser('~')
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('fornt_end.ui', self)
        self.show()
        # self.setupUi(self)
        self.btn1.clicked.connect(self.ftn)
        self.browse_btn.clicked.connect(self.ftn2)
        self.clear_btn.clicked.connect(self.clear)


        self.fname = ""
        # self.label.setText("Please select audio process Mode...")

    def clear(self):
        self.result_prompt.setText("")
        self.xml_path_txt.setText("")
        self.output_csv_path_txt.setText("")




    def ftn2(self):
        # fname = QFileDialog.getOpenFileNames(self, 'Open file', './', 'Wav File (*.wav)')
        self.fname=QFileDialog.getExistingDirectory(self, 'Select directory')
        self.xml_path_txt.setText(self.fname)
        # time_text = self.time_txt.text()
        print(self.fname)
    def ftn(self):
        # time_text = self.time_txt.text()
        print(self.fname)
        xml_path = self.fname
        # Output CSV file
        csv_file = self.output_csv_path_txt.text()
        path_of_image_for_anotation_dot_txt = xml_path
        reset_image_path = xml_path

        def parse_xml(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Initialize lists to store bounding box coordinates and labels
            boxes = []
            labels = []

            for obj in root.findall('object'):
                label = obj.find('name').text
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)

                # Append bounding box coordinates and label
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(label)

            return boxes, labels

        # Directory containing XML annotations
        xml_dir = xml_path
        # Open CSV file for writing
        with open(csv_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Write header row
            csvwriter.writerow(['image_path', 'xmin', 'ymin', 'xmax', 'ymax', 'class'])

            # Iterate through XML files
            for xml_file in os.listdir(xml_dir):
                if xml_file.endswith('.xml'):
                    xml_path = os.path.join(xml_dir, xml_file)
                    boxes, labels = parse_xml(xml_path)

                    # Get the image file path (assuming it's in the same directory)
                    image_path = os.path.splitext(xml_file)[0] + '.jpg'
                    image_path = os.path.join(reset_image_path, image_path)

                    # Write each object's data to the CSV file
                    for i in range(len(boxes)):
                        csvwriter.writerow([image_path] + boxes[i] + [labels[i]])

        ##################################generate annotation dot txt file###############################################

        # Input CSV file
        csv_file = self.output_csv_path_txt.text()

        # Output annotation.txt file
        annotation_file = 'annotation.txt'

        # Open the annotation.txt file for writing
        with open(annotation_file, 'w') as f:
            # Open the CSV file for reading
            with open(csv_file, 'r') as csvf:
                csvreader = csv.reader(csvf)
                for row in csvreader:
                    print(row)
                    # print(len(row))
                    # if len(row) != 7:
                    #     continue  # Skip rows with incorrect format

                    print(row)
                    # Extract information from the CSV row
                    image_path, xmin, ymin, xmax, ymax, label = row

                    # Format the annotation line for Faster R-CNN
                    annotation_line = f"{image_path},{xmin},{ymin},{xmax},{ymax},{label}\n"

                    # Write the annotation line to annotation.txt
                    f.write(annotation_line)

        self.result_prompt.setText("annotation generated")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
