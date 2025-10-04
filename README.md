# SPATUIM - Terra NASA Satellite Project

A comprehensive web application for exploring NASA's Terra satellite data, featuring an AI-powered chatbot, interactive 3D models, and educational games.

## 📋 Project Overview

This project consists of three main components:

1. **AI Model** - Python-based machine learning model running on a local network
2. **Backend** - Node.js/TypeScript REST API with AI chatbot integration (Port 3001)
3. **Frontend** - Next.js web application with interactive 3D visualizations

---

## 🚀 Prerequisites

Before running the project, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **npm** or **yarn**
- **Python** (v3.8 or higher) - for AI model
- **MongoDB** (for backend database)
- **Google AI API Key** - Get it from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 📦 Installation & Setup

### 1️⃣ AI Model (Python)

The AI model folder will be added to the project. Once available, follow these steps:

```bash
# Navigate to the AI model directory
cd ai-model

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the AI model
python app.py
```

> **Note:** The AI model runs on a local network and communicates with both the frontend and backend. Make sure it's running before starting the other components.

---

### 2️⃣ Backend (Node.js + TypeScript)

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
npm install

# Create .env file
# Copy the example or create a new one
```

#### Backend Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Server Configuration
PORT=3001

# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017/terra-db

# Google Generative AI API Key
GOOGLE_GENAI_API_KEY=your_google_api_key_here

# CORS Origin (Frontend URL)
CORS_ORIGIN=http://localhost:3000
```

> **Important:** Get your Google Generative AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and replace `your_google_api_key_here` with your actual API key.

#### Seed Database (Optional)

To populate the database with sample Terra satellite data:

```bash
npm run seed
```

#### Run Backend

```bash
# Development mode (with hot reload)
npm run dev

# Production mode
npm run build
npm start
```

The backend server will start on `http://localhost:3001`

---

### 3️⃣ Frontend (Next.js)

```bash
# Navigate to the frontend directory
cd Nasa-2025

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend application will start on `http://localhost:3000`

#### Frontend Environment Variables (Optional)

Create a `.env.local` file in the `Nasa-2025` directory if you need custom configurations:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:3001

# AI Model URL (if different)
NEXT_PUBLIC_AI_MODEL_URL=http://localhost:5000
```

---

## 🎯 Running the Complete Project

To run the entire project, you need to start all three components. You can do this in two ways:

### ⚡ Quick Start - Run All Projects in Parallel (Recommended)

The easiest way to run all three projects is to open **multiple terminal windows/tabs** and run each component simultaneously:

#### **Terminal 1: MongoDB**
```bash
# Windows (if MongoDB is installed as a service)
net start MongoDB

# macOS (using Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

#### **Terminal 2: AI Model (Python)**
```bash
cd ai-model
# Activate virtual environment
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Run the AI model
python app.py
```
> Keep this terminal running. The AI model will be available at `http://localhost:5000` (or configured port)

#### **Terminal 3: Backend (Node.js)**
```bash
cd backend
npm run dev
```
> Keep this terminal running. Backend API will be available at `http://localhost:3001`

#### **Terminal 4: Frontend (Next.js)**
```bash
cd Nasa-2025
npm run dev
```
> Keep this terminal running. Frontend will be available at `http://localhost:3000`

#### **Access the Application**
Once all three services are running, open your browser and navigate to:
- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **AI Model**: http://localhost:5000
- **API Documentation (Swagger)**: http://localhost:3001/api-docs

---

### 📝 Alternative: Step-by-Step Sequential Startup

If you prefer to start services one at a time and verify each is working:

### Step 1: Start MongoDB

Make sure MongoDB is running on your system:

```bash
# Windows (if MongoDB is installed as a service)
net start MongoDB

# macOS (using Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Step 2: Start the AI Model

```bash
cd ai-model
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
python app.py
```

✅ **Wait until you see:** AI model server starting message (e.g., "Running on http://127.0.0.1:5000")

### Step 3: Start the Backend

Open a new terminal window:

```bash
cd backend
npm run dev
```

✅ **Wait until you see:** `Server running on port 3001`

### Step 4: Start the Frontend

Open another terminal window:

```bash
cd Nasa-2025
npm run dev
```

✅ **Wait until you see:** `Ready - started server on 0.0.0.0:3000`

### Step 5: Access the Application

Open your browser and navigate to: **http://localhost:3000**

---

### 🖥️ Using Windows Terminal (Recommended for Windows Users)

If you're using **Windows Terminal**, you can split panes to run all services in one window:

1. Open Windows Terminal
2. Split into 4 panes (Right-click → Split Pane or use `Alt+Shift++` and `Alt+Shift+-`)
3. In each pane, navigate to the project root and run:
   - **Pane 1**: `cd ai-model && venv\Scripts\activate && python app.py`
   - **Pane 2**: `cd backend && npm run dev`
   - **Pane 3**: `cd Nasa-2025 && npm run dev`
   - **Pane 4**: Keep for commands/monitoring

---

### 🍎 Using iTerm2 or Terminal (macOS/Linux)

For macOS users with **iTerm2** or standard **Terminal**:

1. Open iTerm2/Terminal
2. Create multiple tabs (`Cmd+T` for new tab)
3. In each tab, navigate and run:
   - **Tab 1**: `cd ai-model && source venv/bin/activate && python app.py`
   - **Tab 2**: `cd backend && npm run dev`
   - **Tab 3**: `cd Nasa-2025 && npm run dev`

---

### 🔄 Using Concurrent Processes (Advanced)

You can also use tools like `concurrently` or `npm-run-all` to run multiple npm scripts in parallel.

#### Option 1: Install concurrently in the root
```bash
# In the project root
npm install -g concurrently

# Create a start script that runs all services
concurrently "cd backend && npm run dev" "cd Nasa-2025 && npm run dev"
```

#### Option 2: Create a root package.json
Create a `package.json` in the project root:

```json
{
  "name": "spatuim-root",
  "version": "1.0.0",
  "scripts": {
    "dev:backend": "cd backend && npm run dev",
    "dev:frontend": "cd Nasa-2025 && npm run dev",
    "dev:all": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "install:all": "cd backend && npm install && cd ../Nasa-2025 && npm install"
  },
  "devDependencies": {
    "concurrently": "^8.2.0"
  }
}
```

Then run:
```bash
npm install
npm run dev:all
```

> **Note:** You'll still need to run the AI model separately in its own terminal.

---

### ✅ Verification Checklist

Before testing the application, ensure all services are running:

- [ ] **MongoDB** is running (check with `mongod --version`)
- [ ] **AI Model** is running on port 5000 (or configured port)
- [ ] **Backend** is running on port 3001
- [ ] **Frontend** is running on port 3000
- [ ] No error messages in any terminal
- [ ] You can access http://localhost:3000 in your browser

---

### 🛑 Stopping All Services

To stop all services gracefully:

1. In each terminal window, press `Ctrl+C` to stop the service
2. For MongoDB:
   - **Windows**: `net stop MongoDB`
   - **macOS**: `brew services stop mongodb-community`
   - **Linux**: `sudo systemctl stop mongod`
3. Deactivate Python virtual environment: `deactivate`

---

## 🏗️ Project Structure

```
SPATUIM/
├── ai-model/               # Python AI model (to be added)
│   ├── app.py             # Main AI model server
│   ├── requirements.txt   # Python dependencies
│   └── models/            # Trained models
│
├── backend/               # Node.js backend
│   ├── src/
│   │   ├── server.ts      # Express server entry point
│   │   ├── config/        # Database & Swagger config
│   │   ├── controllers/   # Route controllers
│   │   ├── models/        # MongoDB models (ASTER, CERES, MISR, etc.)
│   │   ├── routes/        # API routes
│   │   ├── services/      # AI service integration
│   │   └── scripts/       # Database seeding scripts
│   ├── .env               # Environment variables
│   └── package.json
│
└── Nasa-2025/             # Next.js frontend
    ├── src/
    │   ├── app/           # Next.js app router
    │   │   ├── api/       # API routes
    │   │   ├── games/     # Game pages
    │   │   └── instruments/ # Instrument details
    │   ├── components/    # React components
    │   ├── sections/      # Page sections
    │   └── utils/         # Utility functions
    ├── public/
    │   └── assets/        # Images, 3D models, videos
    └── package.json
```

---

## 🔌 API Endpoints

### Backend API (Port 3001)

#### Terra Satellite Data
- `GET /api/terra/aster` - ASTER instrument data
- `GET /api/terra/ceres` - CERES instrument data
- `GET /api/terra/misr` - MISR instrument data
- `GET /api/terra/modis` - MODIS instrument data
- `GET /api/terra/mopitt` - MOPITT instrument data

#### AI Chatbot
- `POST /api/message` - Send message to AI chatbot
  ```json
  {
    "message": "What is Terra satellite?"
  }
  ```

#### Health Check
- `GET /health` - Server health status

---

## 🎮 Features

- **Interactive 3D Models** - Explore Terra satellite in 3D using Three.js
- **AI Chatbot** - Ask questions about Terra satellite using Google Generative AI
- **Educational Games**
  - Terra Flash Cards
  - City Builder Game
  - Satellite Data Explorer
- **Instrument Explorer** - Detailed information about Terra's five instruments
- **Weather Predictions** - AI-powered weather predictions using NASA data
- **Mission Timeline** - Visual timeline of Terra's mission

---

## 🛠️ Development

### Backend Scripts

```bash
npm run dev      # Start development server with hot reload
npm run build    # Build TypeScript to JavaScript
npm start        # Start production server
npm run seed     # Seed database with Terra data
```

### Frontend Scripts

```bash
npm run dev      # Start Next.js development server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

---

## 🐛 Troubleshooting

### Backend not connecting to MongoDB
- Ensure MongoDB is running: `mongod --version`
- Check MongoDB connection string in `.env`

### AI Chatbot not responding
- Verify Google AI API key is correct in backend `.env`
- Check API key permissions at [Google AI Studio](https://aistudio.google.com/app/apikey)

### Frontend can't connect to backend
- Ensure backend is running on port 3001
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### Port already in use
- Backend: Change `PORT` in backend `.env`
- Frontend: Run `npm run dev -- -p 3001` to use a different port

### AI Model not accessible
- Ensure Python virtual environment is activated
- Check if the AI model server is running
- Verify network settings and firewall rules

---

## 📝 Environment Variables Summary

### Backend (.env)
```env
PORT=3001
MONGODB_URI=mongodb://localhost:27017/terra-db
GOOGLE_GENAI_API_KEY=your_api_key_here
CORS_ORIGIN=http://localhost:3000
```

### Frontend (.env.local) - Optional
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_AI_MODEL_URL=http://localhost:5000
```

---

## 📚 Technologies Used

### Backend
- Node.js & Express
- TypeScript
- MongoDB & Mongoose
- Google Generative AI (@google/genai)
- Swagger UI (API documentation)

### Frontend
- Next.js 15
- React 19
- Three.js & React Three Fiber
- Tailwind CSS
- Framer Motion
- Axios

### AI Model
- Python
- Machine Learning frameworks (details in AI model folder)

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is part of NASA Space Apps Challenge.

---

## 🙏 Acknowledgments

- NASA for Terra satellite data
- Google AI for Generative AI API
- Next.js team for the amazing framework

---

## 📞 Support

For questions or issues, please open an issue in the repository or contact the development team.

---

**Made with ❤️ for NASA Space Apps Challenge**
