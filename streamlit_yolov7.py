from singleinference_yolov7 import SingleInference_YOLOV7
import os
import streamlit as st
import logging
import requests
from PIL import Image
from io import BytesIO
class Streamlit_YOLOV7(SingleInference_YOLOV7):
    '''
    streamlit app that uses yolov7
    '''
    def __init__(self,):
        self.logging_main=logging
        self.logging_main.basicConfig(level=self.logging_main.DEBUG)

    def new_yolo_model(self,img_size,path_yolov7_weights,path_img_i,device_i='cpu'):
        '''
        SimpleInference_YOLOV7
        created by Steven Smiley 2022/11/24

        INPUTS:
        VARIABLES                    TYPE    DESCRIPTION
        1. img_size,                    #int#   #this is the yolov7 model size, should be square so 640 for a square 640x640 model etc.
        2. path_yolov7_weights,         #str#   #this is the path to your yolov7 weights 
        3. path_img_i,                  #str#   #path to a single .jpg image for inference (NOT REQUIRED, can load cv2matrix with self.load_cv2mat())

        OUTPUT:
        VARIABLES                    TYPE    DESCRIPTION
        1. predicted_bboxes_PascalVOC   #list#  #list of values for detections containing the following (name,x0,y0,x1,y1,score)

        CREDIT
        Please see https://github.com/WongKinYiu/yolov7.git for Yolov7 resources (i.e. utils/models)
        @article{wang2022yolov7,
            title={{YOLOv7}: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors},
            author={Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark},
            journal={arXiv preprint arXiv:2207.02696},
            year={2022}
            }
        
        '''
        super().__init__(img_size,path_yolov7_weights,path_img_i,device_i=device_i)
    def main(self):
        st.title('Toy prediction?')
        st.subheader('Upload an image and run Yolov7:  it will return the toy it thinks is most likely')
        self.response=requests.get(self.path_img_i)
        self.img_screen=Image.open(BytesIO(self.response.content))
        st.image(self.img_screen, caption=self.capt, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
        st.markdown('YoloV7 on streamlit.  Demo of deeplearning with object detection of tanks.')
        self.load_image_st()
        self.predict()

    
    def load_image_st(self):
        self.uploaded_img=st.file_uploader(label='Upload an image to test')
        if self.uploaded_img != None:
            self.img_data=self.uploaded_img.getvalue()
            st.image(self.img_data)
            self.im0=Image.open(BytesIO(self.img_data))
            return self.im0
        elif self.im0 !=None:
            return self.im0
        else:
            return None
    
    def predict(self):
        st.write('loaded iamge in the model')
        self.load_cv2mat()
        self.inference()
        self.show()
        self.img_screen=Image.fromarray(self.image)
        self.capt='DETECTED'
        st.image(self.img_screen, caption=self.capt, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    


        


if __name__=='__main__':
    app=Streamlit_YOLOV7()

    #INPUTS for YOLOV7
    img_size=640
    path_yolov7_weights="weights/best.pt"
    path_img_i=r"https://github.com/stevensmiley1989/STREAMLIT_YOLOV7/blob/main/test_images/DJI_0028_fps24_frame00000040.jpg"
    #INPUTS for webapp
    app.capt="A few of my toys"
    app.new_yolo_model(img_size,path_yolov7_weights,path_img_i)
    app.load_model() #Load the yolov7 model
    app.read_img(path_img_i) #read in the jpg image from the full path, note not required if you want to load a cv2matrix instead directly
    app.main()

    # app.load_cv2mat() #load the OpenCV matrix, note could directly feed a cv2matrix here as app.load_cv2mat(cv2matrix)
    # app.inference() #make single inference
    # app.show() #show results
    # print(f'''
    # app.predicted_bboxes_PascalVOC\n
    # \t name,x0,y0,x1,y1,score\n
    # {app.predicted_bboxes_PascalVOC}''') 