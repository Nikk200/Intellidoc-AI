Got it! Here’s the updated README without environment variable instructions:

---

# IntelliDoc AI

**IntelliDoc AI** is an Intelligent Document Processing System designed to extract text from documents, process the extracted information using AI models, and store the results in a database. This project is built using Django, Python OCR libraries, and AI technologies, and integrates with MySQL/MariaDB.

## Features

- **User Management**: Registration, login, and profile management.
- **Document Upload**: Upload documents for processing.
- **OCR Integration**: Extract text from uploaded documents.
- **AI Processing**: Analyze extracted text using AI models.
- **Database Storage**: Store extracted and processed information in MySQL/MariaDB.
- **Asynchronous Processing**: Handle large documents and heavy tasks using Celery.
- **Progress Updates**: Notify users about the processing status.

## Requirements

- Python 3.8+
- Django 4.0+
- Celery 5.0+
- Redis (for Celery result backend)
- MySQL/MariaDB
- Python OCR libraries (e.g., Tesseract)
- AI libraries (e.g., Hugging Face Transformers)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/intellidoc-ai.git
   cd intellidoc-ai
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Start Celery Worker**

   In a new terminal window:

   ```bash
   celery -A intellidoc_ai worker --loglevel=info
   ```

## Usage

- **Register** a new account or **login** if you already have an account.
- **Upload** documents for text extraction and AI processing.
- Monitor the **processing status** through the user interface.

## Testing

To run tests for the project:

```bash
python manage.py test
```

## Contributing

If you'd like to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Django**: Web framework for Python.
- **Celery**: Asynchronous task queue.
- **Redis**: In-memory data structure store.
- **MySQL/MariaDB**: Relational database management system.
- **Tesseract**: OCR engine.
- **Hugging Face Transformers**: AI models for text processing.

---

Adjust the placeholder `yourusername` as needed.
