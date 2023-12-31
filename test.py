import threading
import keyboard  # Import the keyboard module for key press detection

def transcribe_audio_until_a(language_code, silence_timeout=5):
   recognizer = sr.Recognizer()  # Initialize the recognizer

   def listen_for_audio():
       with sr.Microphone() as source:
           print("######### Listening .......  #######")
           recognizer.adjust_for_ambient_noise(source)

           while True:
               try:
                   audio = recognizer.listen(source, timeout=silence_timeout)
                   text = recognizer.recognize_google(audio, language=language_code)
                   print(text)  # Print the transcribed text

               
               except sr.UnknownValueError:
                   print("Could not understand audio")
               except sr.RequestError as e:
                   print(f"Could not request results from Google Speech Recognition service; {e}")
               except KeyboardInterrupt:
                   print("Stopping transcription...")
                   break  # Exit the loop if a keyboard interrupt occurs

   listen_thread = threading.Thread(target=listen_for_audio)
   listen_thread.start()

   try:
       keyboard.wait("a")  # Wait for the "A" key to be pressed
   except KeyboardInterrupt:
       print("Stopping transcription...")

   listen_thread.join()  # Wait for the listening thread to finis


print(start)
answer = transcribe_audio_until_a("en", silence_timeout=3)
print(answer)