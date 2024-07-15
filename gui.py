import streamlit as st
from PIL import Image as Img
import base64
import time
from mapping import FoliumMap
from landmark_detection import GoogleCloudVision, MockGoogleCloudVision
from ai_summary import MockOpenAI_LLM, AI_Summary
from firestore import Firestore
from streamlit_folium import st_folium

SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp"]
DEBUG_MODE_WARNING_ENABLED = True


class Landmarker:
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        self.gc = self.init_google_cloud_vision()
        self.fm = self.init_folium_map()
        self.summarizer = self.init_TogetherAI()
        self.firestore_connection = self.init_firestore()
        self.set_page_config()
        st.html("""
        <style>
        [data-testid=collapsedControl]::after {
            content: "Open Sidebar";
            position: absolute;
            left: 100%; /* Position the text to the right of the element */
            top: 44%; /* Align the top of the text at the middle of the button */
            transform: translateY(-50%); /* Center the text vertically */
            white-space: nowrap; /* Ensure the text does not wrap */
            margin-left: 10px; /* Space between the text and the element */
            
            /* New gradient background */
            color: hsla(330, 36%, 53%, 1);
        }
        """,)

    def init_google_cloud_vision(self):
        if self.debug:
            return MockGoogleCloudVision()
        else:
            return GoogleCloudVision()

    def init_TogetherAI(self):
        if self.debug:
            return MockOpenAI_LLM()
        else:
            return AI_Summary()

    def init_folium_map(self):
        return FoliumMap()

    def init_firestore(self):
        return Firestore()

    def set_page_config(self):
        st.set_page_config(
            page_title="Landmark Detection",
            page_icon="logo.png",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                "Get Help": "mailto:landmarker+elshad.sabziyev@yahoo.com",
                "Report a Bug": "https://www.github.com/elshadsabziyev/landmarker/issues",
                "About": """
                # Land~Marker
                ### Created by:
                - [Elshad Sabziyev](https://www.github.com/elshadsabziyev)
                """,
            },
        )

    def main(self):
        if self.debug and DEBUG_MODE_WARNING_ENABLED:
            st.warning(
                """
                ## Warning: Debug mode is on.
                - Debug mode is on. (See the sidebar)
                """
            )
            st.sidebar.warning(
                """
                ### Warning: Debug mode is on.
                - Debug mode is on.
                - This mode is only for testing the app.
                - Please do not use this mode unless you are testing the app.
                """
            )
        title = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Major+Mono+Display&display=swap');
            .title {
                font-family: 'Major Mono Display', monospace;
                background: linear-gradient(270deg, rgba(34,193,195,1), rgba(253,187,45,1));
                background-size: 200% 200%;
                animation: gradient 5s ease infinite;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                top: 0px;
                font-size: 4.0em;
            }
            @keyframes gradient {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
            .title {
                animation: gradient 2.5s ease-in-out infinite;
            }
        </style>
        <div class="title">
        LAND~ MARKER
        </div>
        """
        st.markdown(title, unsafe_allow_html=True)
        with st.sidebar.expander("_**Click here to toggle the help view**_", expanded=False):
            st.write("""
# Welcome to the Landmark Detection App!
This app uses Google Cloud Vision to detect landmarks in images.
## How to use this app:
1. **Upload an image**: Use the upload widget to upload an image of a landmark. The image should be in a common format like JPEG or PNG.
2. **Wait for the app to process the image**: The app will send the image to Google Cloud Vision, which will analyze the image and identify any landmarks it contains. This process may take a few seconds.
3. **View the results**: The app will display the landmarks detected by Google Cloud Vision.
## Tips for best results:
- Use clear, high-resolution images. The better the quality of the image, the more likely it is that Google Cloud Vision will be able to identify the landmark.
- Try to make sure the landmark is the main focus of the image. If the landmark is in the background or partially obscured, it may be harder for Google Cloud Vision to identify it.
- Google Cloud Vision can identify many famous landmarks, like the Eiffel Tower or the Grand Canyon. If you're not sure what to upload, try starting with a picture of a well-known landmark.
We hope you enjoy using the Landmark Detection App!
""")
        gc = self.gc
        fm = self.fm
        with st.sidebar.container(border=True):
            camera = st.toggle(
                label="Camera", value=False, help="Switch on the camera."
            )
        if camera:
            st.warning(
                """
                ### Privacy Warning: Camera is on.
                - Please make sure you are pointing the camera at a landmark.
                - The camera will take a snapshot when you click on the upload button.
                """
            )
            try:
                with st.sidebar.expander("_Please point the camera at a **landmark**._", expanded=True):
                    uploaded_file = st.camera_input(
                        label="Take a snapshot of a landmark.",
                        label_visibility="collapsed",
                    )
            except Exception as e:
                st.warning(
                    f"""
                    ### Error: Camera could not be turned on.
                    - Error Code: 1x000
                    - There may be issues with your camera.
                    - Try enabling the camera in your browser/OS settings.
                    - You can manually upload an image of a landmark.
                    - If the problem persists, it's not your fault, probably.
                    - Please try again. If the problem persists, please contact the developer.
                    """
                )
        else:
            try:
                with st.sidebar.expander("_Please upload an image of a **landmark**._", expanded=True):
                    uploaded_file = st.file_uploader(
                        type=SUPPORTED_FORMATS,
                        accept_multiple_files=False,
                        help="Upload an image of a landmark.",
                        label_visibility="collapsed",
                        label="Upload Image",
                    )

            except Exception as e:
                st.warning(
                    f"""
                    ### Error: Image could not be uploaded.
                    - Error Code: 1x001
                    - There may be issues with your image.
                    - Please make sure you have uploaded a valid image.
                    - Please make sure the image is in one of the supported formats (png, jpg, jpeg, webp).
                    - Please try again. If the problem persists, please contact the developer.
                    """
                )
        if uploaded_file is not None:
            image = Img.open(uploaded_file)
            with st.sidebar.status("Processing the image...", expanded=False) as status:
                st.image(
                    image,
                    caption="Uploaded Image",
                    use_column_width=True,
                )
                status.update(
                    state="complete",
                    label="_Image Processed_ : **Go to the main page to see the results.**",
                    expanded=True,
                )
        else:
            with st.expander("_**Click here to toggle the help view**_", expanded=True):
                st.markdown(
                    """
                    ### Instructions:
                    - _**Click** on the **>** icon on the **top left corner** of the app to expand the sidebar._
                    - _**Upload** an image of a landmark using the upload **widget** on the sidebar._
                    """,
                    unsafe_allow_html=True,
                )
        landmark_most_matched = ""
        landmark_most_matched_score = 0
        lat_most_matched = 0
        lon_most_matched = 0
        if uploaded_file is not None:
            landmarks = gc.find_landmark(uploaded_file)
            for landmark in landmarks:
                landmark_name = landmark.description
                confidence = "Matched: " + \
                    str(round(landmark.score * 100, 2)) + "%"
                lat = landmark.locations[0].lat_lng.latitude
                lon = landmark.locations[0].lat_lng.longitude
                fm.add_marker(lat, lon, landmark_name, confidence)
                fm.add_heatmap(lat, lon, landmark.score)
                if landmark.score > landmark_most_matched_score:
                    landmark_most_matched_score = landmark.score
                    landmark_most_matched = landmark_name
                    lat_most_matched = lat
                    lon_most_matched = lon
            try:
                map_html = fm.map._repr_html_()
            except Exception as e:
                st.error(
                    f"""
                    ### Error: Map could not loaded.
                    - Error Code: 1x002
                    - Most likely, it's not your fault.
                    - Please try again. If the problem persists, please contact the developer.
                    """
                )
                st.stop()
            try:
                fm.map.fit_bounds(fm.map.get_bounds(), padding=[
                                  40, 40], max_zoom=17)
            except Exception as e:
                st.warning(
                    f"""
                    ### Error: Map could not be adjusted.
                    - Error Code: 1x003
                    - Most likely, it's not your fault.
                    - Please try again, or zoom out a bit to see the whole map.
                    - You can also rerun the app to see if the problem persists.
                    - If the problem persists, please contact the developer.
                    """
                )
            if landmarks:
                a = """ - **Zoom out to see the whole map, or just download it.**"""
                b = """ - **Click on the markers to see the landmark name and similarity score.**"""
                c = """ - **Click on the download button to download the map.**"""
                d = """ - **Toggle the satellite map switch to see the map in satellite mode.**"""
                e = """ - **Toggle the stream summary switch to see the summary stream.**"""
                with st.expander("**Click here to see the instructions.**"):
                    st.write(a + "\n" + b + "\n" + c + "\n" + d + "\n" + e)
                    st.write(
                        """
                        ---
                        PIN COLOR GUIDE:
                        - **Red Pin**: Low confidence
                        - **Yellow Pin**: Medium confidence
                        - **Green Pin**: High confidence
                        """
                    )
                with st.expander("**Click here to change the app settings.**"):
                    col1, col2 = st.columns(2)
                    with col1:
                        satellite_mode = st.toggle(
                            "Satellite Map",
                            False,
                            help="Switch on the satellite mode.",
                        )
                    with col2:
                        stream_mode = st.toggle(
                            "Stream Summary",
                            False,
                            help="Switch on for streaming the summary as it's being generated. It bypasses the caching and get fresh summary in real-time.",
                        )
                    if stream_mode:
                        st.session_state["summary_stream"] = True
                    else:
                        st.session_state["summary_stream"] = None
                _ = fm.satellite_map() if satellite_mode else None
            else:
                pass
            PREVIOUS_CITY_COUNTRY = ("Kövsər Dönər", "28 May")
            if landmarks:
                city, country = fm.get_city_country(lat, lon)
                if city and country:
                    if (city, country) != PREVIOUS_CITY_COUNTRY:
                        with st.status("**Identifying the location...**", expanded=False) as status:
                            st.write(
                                f"""
                                ## {landmark_most_matched}
                                """
                            )
                            status.update(state="complete",
                                          label=f"_Location Identified_ : **{city}, {country}**", expanded=True)
                            try:
                                prompt = f"Craft a professional and concise 80-word summary about {landmark_most_matched} in {city}, {country}. Include the origin of its name, historical significance, and cultural impact. Share fascinating facts that make it a must-visit for tourists."
                                if st.session_state.get("summary_stream") is not None:
                                    st.write_stream(
                                        self.summarizer.stream_summary(prompt))
                                    time.sleep(0.10)
                                else:
                                    with st.spinner("Generating LLM Based Summary..."):
                                        summary = self.summarizer.generate_summary(
                                            prompt)
                                        # write summary in bold
                                        st.markdown(
                                            f"**{str(summary).strip()}**"
                                        )
                                st.warning(
                                    """
                                    ###### The LLM Based Summary is generated by the AI model.
                                    - The summary may not be accurate, please verify the information before using it.
                                    """
                                )
                            except Exception as e:
                                st.error(
                                    f"""
                                    ### Error: LLM Based Summary could not be generated.
                                    - Error Code: 1x004
                                    - Most likely, it's not your fault.
                                    - Please try again. If the problem persists, please contact the developer.
                                    """
                                )
                                st.stop()
                        PREVIOUS_CITY_COUNTRY = (city, country)
                else:
                    st.write(
                        """
                        # Unknown Location
                        """
                    )
                help_text = (
                    """Satalite map is not available for download. What you are going to download is the normal map."""
                    if satellite_mode
                    else """Download the map to see the whole map."""
                )
                lat = lat_most_matched
                lon = lon_most_matched
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    st.link_button(
                        label="Open Google Maps",
                        url=f"https://www.google.com/maps/search/?api=1&query={lat},{lon}",
                        use_container_width=True,
                    )
                wiki_url = (
                    fm.get_wikipedia_page(landmark_most_matched)
                    or f"https://www.google.com/search?q={landmark_most_matched} wikipedia&btnI"
                )
                with col2:
                    st.link_button(
                        label="Open Wiki Page",
                        url=wiki_url,
                        use_container_width=True,
                    )
                    try:
                        col3.download_button(
                            label="Download Map",
                            data=map_html,
                            file_name=f"{landmark_most_matched}_full_screen_map.html",
                            mime="text/html",
                            on_click=st.write(
                                f'<a href="data:text/html;base64,{base64.b64encode(map_html.encode()).decode()}" download="map.html" style="display: none;">Download Map</a>',
                                unsafe_allow_html=True,
                            ),
                            key="normal_map",
                            help=help_text,
                            use_container_width=True,
                        )
                    except UnboundLocalError:
                        st.write(
                            """
                        > boop-beep-boop...
                        """
                        )
                with st.status("Loading the map...", expanded=False) as status:
                    with st.container(height=460):
                        st_folium(fm.map, use_container_width=True, height=400,
                                  returned_objects=[])
                    status.update(
                        state="complete",
                        label="_Map Loaded_ : **Click on the markers to see the landmark name and similarity score.**",
                        expanded=True,
                    )
                st.write(
                    """ 
                    ## Reviews:
                    """
                )
                with st.spinner("Loading reviews..."):
                    reviews = self.firestore_connection.get_review_for_landmark(
                        lon, lat, 0.1, landmark_most_matched
                    )
                    # Button to add a review
                    with st.expander("**Click here to write a review.**"):
                        with st.form(key="add_review_form"):
                            username = st.text_input(
                                label="Username", help="Enter your username."
                            )
                            review = st.text_area(
                                label="Review", help="Enter your review.")
                            score = st.slider(
                                label="Score",
                                min_value=1,
                                max_value=10,
                                value=5,
                                help="Choose a score.",
                                step=1,
                            )
                            submit_button = st.form_submit_button(
                                label="Submit")
                        if submit_button:
                            if username and review and score:
                                self.firestore_connection.create_new_review(
                                    review,
                                    landmark_most_matched,
                                    f"{lon}/{lat}",
                                    score,
                                    username,
                                )
                                st.success("- Review added successfully.")
                                st.rerun()
                            else:
                                st.warning("- Please fill in all the fields.")
                    with st.expander(
                        "**Click here to see the reviews for this landmark.**"
                    ):
                        if reviews:
                            for review in reviews:
                                def mask_username(username):
                                    words = username.split()
                                    masked_words = []
                                    for word in words:
                                        if len(word) > 3:
                                            masked_word = word[:2] + "\\*" * \
                                                (len(word) - 3) + word[-1]
                                        else:
                                            masked_word = word
                                        masked_words.append(masked_word)
                                    return ' '.join(masked_words)
                                st.markdown(
                                    f"##### {mask_username(review['Username'])}")
                                st.markdown(
                                    f""" {"**Excellent**" if review['Score10'] >= 9 else "**Good**" if review['Score10'] >= 7 else "**Average**" if review['Score10'] >= 5 else "**Poor**" if review['Score10'] >= 3 else "**Terrible**"} ({"⭐" * 1 if review['Score10'] <= 2 else "⭐" * 2 if review['Score10'] <= 4 else "⭐" * 3 if review['Score10'] <= 6 else "⭐" * 4 if review['Score10'] <= 8 else "⭐" * 5})"""
                                )
                                st.markdown(f"> {review['Review']}")
                                st.markdown("---")
                        else:
                            st.write(
                                """
                                - No reviews yet. Be the first one to review this landmark!
                                """
                            )
                    with st.expander("**Click here to see AI generated review summary.**", expanded=True):
                        if reviews:
                            prompt = f"Craft a professional and concise 2-3 sentence review summary about {landmark_most_matched} in {city}, {country} considering the reviews: {', '.join([r['Review'] for r in reviews])}. Focus on verifiable information and avoid claims without evidence (e.g., rumors, speculation). At the end mention unverifiable/unrelated claims if any."
                            summary = self.summarizer.summarize_review(prompt)
                            summary = str(summary).strip()
                            st.write(
                                f"Overall Score: {round(sum([r['Score10'] for r in reviews])/len(reviews), 2)}"
                            )
                            st.write(
                                f"""
                                > **{summary}**
                                """
                            )
                            st.warning(
                                """
                                ###### The review summary is generated by the AI model.
                                - The summary is generated based on the reviews.
                                - It may not be accurate, please verify the information before using it.
                                """
                            )
                        else:
                            st.write(
                                """
                                - No reviews yet. Be the first one to review this landmark!
                                """
                            )
            else:
                st.write(
                    """
                    # Oops! No landmarks detected.
                    ## Possible reasons:
                    - The image is not of a landmark.
                    - The landmark is not famous enough.
                    - The image is not clear enough.
                    """
                )
        for i in range(4):
            st.write("")
        footer = """
        ---
        ###### Made with 💗 using _[Streamlit](https://www.streamlit.io/), [Google Cloud Vision](https://cloud.google.com/vision)_, _[Folium](https://python-visualization.github.io/folium/)_ and _[TogetherAI](https://api.together.ai/)_.
        """
        st.markdown(footer, unsafe_allow_html=True)
