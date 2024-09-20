# 🎥 Video Upload, Subtitle Extraction & Search API (Play from Subtitle Timestamp)

## 📖 Overview
A Django-based API that enables users to upload videos, extract subtitles, and search for phrases within subtitles. Users can play videos starting from the timestamp where the searched phrase is found. The system supports asynchronous processing using Celery and Redis for efficient handling.

## ✨ Features
- **Upload Videos**
- **Extract Subtitles** using `ffmgpeg`
- **Asynchronous Processing** with Celery

## ⚙️ Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## 📥 Installation

### Without Docker
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/video-upload-project.git
   cd video-upload-project

2. **Create a Virtual Environment:**

   ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Install Dependencies:**
   ```bash
    pip install -r requirements.txt
   
4. **Setup Database:**
   
   Create a postgres database and update settings.py.


5. **Start Redis:**
   ```bash
   redis-server
   
6. **Migrate Database:**
   ```bash
   python manage.py migrate

7. **Start Celery Worker:**
   ```bash
   celery -A your_project_name worker --loglevel=info
   
8. **Run the Development Server:**
   ```bash
   python manage.py runserver

## With Docker
1. **Build and Run Docker Containers:**
   ```bash
    docker-compose up --build

2. **Access the Application:** 
     Open your browser and go to http://localhost:8000.

## 📡 API Endpoints

1. **Upload Video**
   - **POST** `/upload/`
   - Uploads a new video. Expects a video file and a title.
   - **Request Body:**
     - `video`: Video file (multipart/form-data)
     - `title`: Video title (string)

2. **List All Videos**
   - **GET** `/`
   - Retrieves a list of all uploaded videos, ordered by the latest upload first.
   - **Response:** List of video objects with metadata (e.g., title, upload date).

3. **Get Video Details**
   - **GET** `/video/<int:pk>/`
   - Retrieves detailed information for a specific video.
   - **Response:** Video details, including associated subtitles.

4. **Get Subtitles for a Video**
   - **GET** `/videos/<int:video_id>/subtitles/`
   - Retrieves a list of subtitles for a specific video.
   - **Response:** List of subtitle entries with timestamps and text.

5. **Search Subtitles by Phrase**
   - **GET** `/videos/<int:video_id>/search_subtitles/`
   - Searches for a phrase within the subtitles and returns the timestamp where the phrase occurs. Video can start playing from that timestamp.
   - **Request Params:** 
     - `phrase`: The subtitle text phrase to search for.
   - **Response:**
     - `timestamp`: The timestamp where the phrase appears in the video.
     - Example:
     ```json
     {
       "timestamp": "00:02:15",
       "text": "This is the phrase"
     }
     ```

## Result Overview
    For an overview of the results, watch the video located in the result_overview folder at the root of the project.

