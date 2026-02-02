# CVMakeover.AI

**CVMakeover.AI** is an AI-powered browser extension that helps job seekers generate **ATS-optimized, role-specific resumes** using a single structured profile and a target job description.

Instead of rewriting resumes from scratch for every application, CVMakeover.AI allows users to tailor how their *existing experience* is presented — efficiently, consistently, and honestly.

---

## 🚀 Inspiration

As graduate students applying to multiple internships and full-time roles, we found ourselves repeatedly customizing resumes for each job description. While the experience stayed the same, the wording, emphasis, and keywords needed constant adjustment.

CVMakeover.AI was built to reduce this repetitive effort and make resume customization a streamlined, repeatable workflow.

---

## ✨ What It Does

- Extracts job descriptions directly from job posting pages
- Uses a structured resume profile as a single source of truth
- Tailors resume content to match job-relevant skills and keywords
- Optionally enhances bullet points using AI (while remaining truthful)
- Generates professional, ATS-friendly **LaTeX resumes**
- Allows users to download ready-to-compile `.tex` files

This tool is **not** about fabricating experience — it focuses on expressing real work more effectively.

---

## 🛠️ How It’s Built

### Frontend
- Chrome Extension for seamless job-page interaction
- JavaScript, HTML, and CSS
- Chrome Extensions API for content extraction and messaging

### Backend
- FastAPI-based REST service
- Structured JSON resume profiles
- Optional LLM integration for bullet rewriting
- Jinja2 + LaTeX templates for resume generation

### Output
- Clean, professional LaTeX resumes suitable for ATS systems
- Easily exportable to PDF

---

## 🧩 Tech Stack

- Python  
- FastAPI  
- JavaScript  
- HTML  
- CSS  
- ChromeExtensionsAPI  
- LaTeX  
- Jinja2  
- GroqAPI  
- JSON  
- Git  
- GitHub  
- Uvicorn  

---

## ⚙️ Project Structure

CVMakeover.AI/

├── backend/ # FastAPI backend and resume generation logic
├── extension/ # Chrome extension UI and content scripts
├── shared/ # Shared schemas and example payloads
├── README.md


---

## 🧪 Running the Project Locally

### Backend
```bash
git checkout backend
python -m venv venv
source venv/bin/activate
python -c "import groq; print('groq OK')"
python -m uvicorn backend.app.main:app --reload --port 8000
```
Visit: http://localhost:8000/docs

### Chrome Extension
```bash
git checkout extension-ui
```
1. Open chrome://extensions
2. Enable Developer mode
3. Click Load unpacked
4. Select the extension/ folder
5. Set backend URL to http://localhost:8000

## Challenges & Learnings

Designing AI-assisted rewriting without exaggeration

Managing parallel frontend and backend development

Handling unstructured resume data consistently

Coordinating development across multiple branches and environments

This project emphasized the importance of clean architecture, ethical AI usage, and incremental development.

## What’s Next

Improved job description parsing

Resume match scoring and feedback

Multiple resume templates

Enhanced extension UI and user input forms

Deployment beyond local development

## Contributors

Sujeeth

Rithika Baskaran

## License
This project was built as part of a hackathon and is intended for educational and demonstration purposes.

