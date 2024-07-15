# LandMarker (Landmark Marker) 🗺️📌

## Table of Contents
- [LandMarker (Landmark Marker) 🗺️📌](#landmarker-landmark-marker-️)
  - [Table of Contents](#table-of-contents)
  - [🌟 Introduction](#-introduction)
  - [⭐ Features](#-features)
  - [💻 Technologies Used](#-technologies-used)
  - [🛠️ Installation](#️-installation)
  - [🚀 Usage](#-usage)
  - [🌐 Deployment](#-deployment)
  - [🏗️ Architecture](#️-architecture)
    - [Components](#components)
    - [Workflow](#workflow)
  - [🛣️ Roadmap](#️-roadmap)
    - [Version 1.0.0 (Initial Release)](#version-100-initial-release)
    - [Version 1.1.0](#version-110)
    - [Version 2.0.0 (Previous Release)](#version-200-previous-release)
    - [Version 2.1.0 (Current Release)](#version-210-current-release)
    - [Version 3.0.0 (Repository Update)](#version-300-repository-update)
    - [Future Enhancements](#future-enhancements)
  - [👨‍💻 Project Team](#-project-team)
  - [🤝 Contributing](#-contributing)
  - [📝 License](#-license)

---

## 🌟 Introduction

LandMarker is a web application that streamlines the process of recognizing and mapping landmarks in images. Developed using Google Cloud Vision API, Streamlit, and Folium, LandMarker aims to provide an efficient and seamless user experience. With its intuitive interface and AI Summary integration powered by TogetherAI, LandMarker enables users to effortlessly upload images, detect landmarks, and visualize them on an interactive map.

This application is built to simplify the landmark mapping process for users. It is designed to the diverse needs of users, from casual image analyzers to enthusiasts seeking precise landmark recognition. Whether you're a history buff fascinated by ancient structures or a traveler seeking to plan your next adventure, LandMarker has got you covered. So, why wait? Explore the world of landmark mapping with LandMarker today!

---

## ⭐ Features

LandMarker offers the following features:
- **Image Upload**: Easily upload images containing landmarks for recognition.
- **Landmark Detection**: Utilizes the Google Cloud Vision API for precise landmark recognition in images.
- **Geographical Mapping**: Retrieves geographical coordinates (latitude and longitude) of detected landmarks.
- **Interactive Map Display**: Exhibits detected landmarks on an interactive map using the Folium library.
- **AI Integration**: Provides a short summary about the landmark using 
- **User Reviews**: Allows users to leave reviews on detected landmarks. 

---

## 💻 Technologies Used

The project utilizes the following technologies:
- **Python**: Core programming language.
- **Google Cloud Vision API**: Empowers the system for landmark detection in images.
- **Folium**: Python library employed for creating interactive maps.
- **Streamlit**: Web application framework facilitating the user interface.
- **TogetherAI API**: Used for providing short summary about the landmark.
- **PIL (Python Imaging Library)**: Utilized for image processing and display.

---

## 🛠️ Installation

To set up and run this project locally, follow these steps:
1. **Clone the repository**.
   - Run the following command to clone the repository to your local machine:
        ```bash
        git clone
        ```
    - Enter the project directory:
        ```bash
        cd LandMarker-WebApp
        ```
2. **Set Up Environment**: Create a virtual environment and install required dependencies.
   - Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    - Activate the virtual environment:
      - For Linux/Mac:
        ```bash
        source venv/bin/activate
        ```
      - For Windows:
        ```bash
        venv\Scripts\activate
        ```
    - Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```

3. **Google Cloud Platform (GCP) Setup**: Establish a GCP project, enable the Vision API, and configure credentials.
    - Create a new project on GCP.
    - Enable the Vision API for the project.
    - Create a service account and download the JSON credentials file.
    - Go to https://www.convertsimple.com/convert-json-to-toml/ and convert the JSON file to TOML format.
    - Save the TOML file as secret.toml under the .streamlit directory.
  
4. **TogetherAI API Setup**: Set up the API key for the TogetherAI API.
    - Create an account on TogetherAI.
    - Navigate to the API Keys page.
    - Enter the API key and paste it in the "API Key" field.

5. **Running the Application**: Execute specific commands to run the Streamlit application.
    - Run the following command to start the application:
        ```bash
        streamlit run app.py
        ```
    - The application will start and provide a URL for accessing the interface.

---

## 🚀 Usage

For local usage, credentials should be stored in a secret.toml file. For deployment on Streamlit Sharing or other hosting platforms, ensure the application is appropriately configured for deployment and follow platform-specific instructions.

---

## 🌐 Deployment

- **For Streamlit Sharing**: Follow these steps to deploy the application on Streamlit Sharing:
    1. Create a GitHub repository with the project files or just fork this repository.
    2. Sign in to Streamlit Sharing and connect your GitHub repository.
    3. While configuring the deployment, ensure the required environment variables are set.
    4. Access the application using the provided URL.
    5. If you have any issues, consult the [Streamlit Sharing Documentation](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html).
- **For Other Platforms**: Consult the documentation for the specific hosting platform for deployment instructions.
  
---

## 🏗️ Architecture

### Components
- **Google Cloud Vision API**: Handles landmark detection in images.
- **TogetherAI API**: Provides short summary about the landmark.
- **GeoCoding API**: Used for getting the name of the City and Country of the landmark using reverse geocoding.
- **Streamlit**: Web application framework for creating the user interface.
- **Folium Map**: Used to display detected landmarks on an interactive map.
- **Python Backend**: Utilizes Streamlit to create the user interface and Folium for map generation.

### Workflow
1. User uploads an image via the Streamlit interface.
2. Python backend sends the image data to the Google Cloud Vision API for landmark detection.
3. The API returns landmark information (name and coordinates).
4. GeoCoding API is used to get the name of the City and Country of the landmark using reverse geocoding from the coordinates.
5. TogetherAI API is used to get a short summary about the landmark using the name of the landmark.
6. Folium library creates an interactive map displaying the detected landmark.

---

## 🛣️ Roadmap

### Version 1.0.0 (Initial Release)
- Basic functionality with landmark detection and mapping features implemented.
- Local deployment and usage instructions provided.
- Integration with Geo API for enhanced mapping capabilities.
- Streamlit hosting guide included.

### Version 1.1.0
- Enhanced user interface and error handling.
- Improved documentation and codebase organization.
- Fix for map responsiveness and display issues.
  
### Version 2.0.0 (Previous Release)
- TogetherAI API integration for short summary about the landmark.
- Streamlit Sharing deployment guide included.
- Enhanced user interface and error handling.
- Improved documentation and codebase organization.
- Additional features and enhancements.
- Bug fixes and performance improvements.
- Updated dependencies and overall system stability.

### Version 2.1.0 (Current Release)
- New theme and styling for the user interface.
- Improved error handling and user feedback.
- Enhanced documentation and codebase organization.
- Cache implementation for improved performance.
- New AI summary provider - TogetherAI.

### Version 3.0.0 (Repository Update)
- Migrated to a new GitHub repository.


### Future Enhancements
- Real-time camera capture capabilities for on-the-fly landmark detection.
- Migration to a more scalable and efficient cloud platform.
- Dropping streamlit and using a more scalable web framework.
- Implementing interface for user feedback and error reporting.
- Implementing user-friendly interface for and AI summary customization.
- Native mobile application for on-the-go landmark detection.
- Integration with additional AI and mapping APIs for enhanced functionality.

---

## 👨‍💻 Project Team

- [Elshad Sabziyev](https://github.com/elshadsabziyev) 👨‍💻
- [Arif Najafov](https://github.com/member-profile) 💡

---

## 🤝 Contributing

Contributions are welcome! Fork the repository, make changes, and submit a pull request.

---

## 📝 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). See the [LICENSE](LICENSE) file for details.

