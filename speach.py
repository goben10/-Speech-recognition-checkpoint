import streamlit as st
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

def transcribe_speech(recognizer, audio, api, language):
    # Function to transcribe speech using the selected API
    try:
        if api == "google":
            return recognizer.recognize_google(audio, language=language)
        elif api == "sphinx":
            return recognizer.recognize_sphinx(audio, language=language)
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from the API; {e}"

def save_transcription(text):
    # Function to save the transcription to a file
    filename = st.text_input("Enter the filename to save the transcription:", "transcription.txt")
    if st.button("Save Transcription"):
        with open(filename, "w") as file:
            file.write(text)
        st.success(f"Transcription saved to {filename}")
        
        # Provide a download button for the saved file
        with open(filename, "r") as file:
            st.download_button(label="Download Transcription", data=file, file_name=filename, mime="text/plain")

def main():
    # Main function to run the Streamlit app
    st.title("Speech Recognition App 🎤")
    st.subheader("Transcribe your speech to text easily and quickly!")

    # Information and settings
    st.sidebar.title("About")
    st.sidebar.info("This app uses the SpeechRecognition library to transcribe speech to text. You can choose between Google Speech Recognition and Sphinx (offline) APIs.")
    
    st.sidebar.title("Contact Info")
    st.sidebar.info("For any queries, contact us at: chizeyfrancis@gmail.com")

    st.sidebar.title("Help")
    st.sidebar.info("For help, visit our [documentation](https://example.com/docs)")

    st.sidebar.title("Links")
    st.sidebar.markdown("[GitHub](https://github.com/1Chizey/Speech-Recognition-checkpoint)")

    # Select the API and language for transcription
    st.header("Settings")
    api = st.radio("Select Speech Recognition API:", ("Google Speech Recognition", "Sphinx (offline)"))
    api = "google" if api == "Google Speech Recognition" else "sphinx"
    language = st.text_input("Enter the language code (e.g., 'en-US' for English, 'fr-FR' for French):", "en-US")

    if st.button("Start Recording"):
        # Start recording the speech
        st.info("Say something...")
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        transcription = transcribe_speech(recognizer, audio, api, language)
        st.write("Transcription: " + transcription)

        # Option to save the transcription
        save_option = st.radio("Do you want to save the transcription to a file?", ("Yes", "No"))
        if save_option == 'Yes':
            save_transcription(transcription)

if __name__ == "__main__":
    main()