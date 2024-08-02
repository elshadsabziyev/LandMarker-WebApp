import pickle
import streamlit as st
from google.cloud import vision
from credentials import Credentials


class GoogleCloudVision(Credentials):

    def __init__(self):
        super().__init__()
        try:
            self.client = vision.ImageAnnotatorClient(credentials=self.GCP_credentials)
        except Exception as e:
            st.error(f"""
                Error: {e}
                ### Error: Invalid credentials.
                - Error Code: 0x002
                - There may be issues with Google Cloud Vision API.
                - Another possible reason is that credentials you provided are invalid or expired.
                - Most likely, it's not your fault.
                - Please try again. If the problem persists, please contact the developer.
                """)
            st.stop()

    def find_landmark(self, image_data):
        image = self._load_image(image_data)
        landmarks = self._detect_landmarks(image)
        return landmarks

    def _load_image(self, image_data):
        try:
            image_data.seek(0)
            image = vision.Image(content=image_data.read())
            return image
        except Exception as e:
            st.error(f"""
                Error: {e}
                ### Error: Invalid image.
                - Error Code: 0x003
                - Please make sure you have uploaded a valid image.
                - Please make sure the image is in one of the supported formats (png, jpg, jpeg, webp).
                - Please try again. If the problem persists, please contact the developer.
                """)
            st.stop()

    def _detect_landmarks(self, image):
        try:
            response = self.client.landmark_detection(image=image)
            landmarks = response.landmark_annotations
            return landmarks
        except Exception as e:
            st.error(f"""
                Error: {e}
                ### Error: Landmark detection failed.
                - Error Code: 0x004
                - There may be issues with Google Cloud Vision API.
                - Another possible reason is that credentials you provided are invalid or expired.
                - Most likely, it's not your fault.
                - Please try again. If the problem persists, please contact the developer.
                """)
            st.stop()


class MockGoogleCloudVision:

    def __init__(self):
        pass

    def find_landmark(self, image_data):
        response = self._load_mock_response()
        landmarks = response.landmark_annotations
        return landmarks

    def _load_mock_response(self):
        with open("response.pkl", "rb") as f:
            response = pickle.load(f)
        return response
