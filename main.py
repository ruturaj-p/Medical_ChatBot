from fastapi import FastAPI, File, UploadFile, HTTPException
from .model import (
    transcribe_audio, get_language_code, translate_text, text_to_audio, first_response,second_response, third_response
)

app = FastAPI()

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/process_audio/")
async def process_audio_route(file: UploadFile = File(...)): 
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, 'wb') as buffer:
            buffer.write(file.file.read())

        language_code = get_language_code("english")  # Defaulting to English
        transcribed_text = transcribe_audio(language_code, temp_file_path)
        os.remove(temp_file_path)

        # Initialize conversation
        # conversation.initialize()  # Assuming initialization is needed


        # Start conversation with initial patient input
        response = first_response(transcribed_text)

        # Loop for two follow-up questions
        for _ in range(1):
            follow_up_question = response

            # Convert follow-up question to speech
            language_code = "en"
            output_path = 'Data'
            output_filename = 'output_audio.wav'
            text_to_audio(follow_up_question, language_code, output_path, output_filename)

            # Return follow-up question and audio path to frontend
            return {
                "follow_up_question": follow_up_question,
                "audio_file_path": os.path.join(output_path, output_filename)
            }

            # Get patient's response (assumed to be received from frontend)
            patient_response = await get_patient_response()  # Replace with actual logic

            # Continue conversation
            response = second_response(patient_response)

        final_response = third_response(response)

        # Final response
        return {"final_response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Replace this placeholder with logic to receive patient's response
async def get_patient_response():
    # Assuming the frontend will make a POST request with either text or audio
    patient_response_data = await request.json()  # Receive JSON data

    if "text" in patient_response_data:
        patient_response = patient_response_data["text"]  # Text response
    else:
        # Assuming audio response is sent as a base64-encoded string
        audio_data = patient_response_data["audio"]
        with open("temp_audio.wav", "wb") as f:
            f.write(base64.b64decode(audio_data))
        patient_response = transcribe_audio("en", "temp_audio.wav")  # Transcribe audio
        os.remove("temp_audio.wav")

    return patient_response

