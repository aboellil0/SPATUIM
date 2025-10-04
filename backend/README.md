# Terra Chatbot Backend

A Node.js + TypeScript backend API for the Terra NASA satellite chatbot using Google Generative AI.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - The API key is already configured

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build the TypeScript project
- `npm start` - Start production server (requires build first)

## API Endpoints

### POST /api/message

Send a message to the Terra chatbot.

**Request Body:**
```json
{
  "message": "What is Terra satellite?"
}
```

**Response:**
Streaming text response from the AI.

**Example using cURL:**
```bash
curl -X POST http://localhost:3000/api/message \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is Terra satellite?\"}"
```

**Example using JavaScript fetch:**
```javascript
const response = await fetch('http://localhost:3000/api/message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What is Terra satellite?'
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  const chunk = decoder.decode(value);
  console.log(chunk);
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

## Running the Server

Development mode:
```bash
npm run dev
```

Production mode:
```bash
npm run build
npm start
```

The server will start on `http://localhost:3000`

## Project Structure

```
backend/
├── src/
│   ├── server.ts              # Main Express server
│   ├── controllers/
│   │   └── messageController.ts   # Message endpoint handler
│   └── services/
│       └── aiService.ts       # Google AI integration
├── dist/                      # Compiled JavaScript (after build)
├── .env                       # Environment variables
├── .env.example              # Environment template
├── tsconfig.json             # TypeScript configuration
└── package.json              # Dependencies and scripts
```
