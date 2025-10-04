import type { Request, Response } from 'express';
import { generateAIResponse, generateQuestionExplanation } from '../services/aiService';

export const messageController = async (req: Request, res: Response): Promise<void> => {
  try {
    const { message } = req.body;

    if (!message || typeof message !== 'string') {
      res.status(400).json({ 
        error: 'Invalid request', 
        details: 'Message field is required and must be a string' 
      });
      return;
    }

    // Set headers for streaming response
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Transfer-Encoding', 'chunked');

    // Generate and stream AI response
    await generateAIResponse(message, (chunk: string) => {
      res.write(chunk);
    });

    res.end();
  } catch (error) {
    console.error('Error in messageController:', error);
    
    if (!res.headersSent) {
      res.status(500).json({ 
        error: 'Internal server error', 
        details: error instanceof Error ? error.message : 'Unknown error' 
      });
    } else {
      res.end();
    }
  }
};

export const explainQuestionController = async (req: Request, res: Response): Promise<void> => {
  try {
    const { question, userAnswer, correctAnswer, options } = req.body;

    // Validate request
    if (!question || !userAnswer || !correctAnswer) {
      res.status(400).json({ 
        error: 'Invalid request', 
        details: 'Question, userAnswer, and correctAnswer fields are required' 
      });
      return;
    }

    // Construct a detailed prompt for the AI
    const prompt = `
Question: ${question}
${options ? `\nAvailable Options:\n${Array.isArray(options) ? options.map((opt: string, idx: number) => `${idx + 1}. ${opt}`).join('\n') : options}` : ''}

Your Answer: ${userAnswer}
Correct Answer: ${correctAnswer}

Please explain why my answer is incorrect and why the correct answer is right.
`;

    // Set headers for streaming response
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Transfer-Encoding', 'chunked');

    // Generate and stream AI response using the specialized question explanation service
    await generateQuestionExplanation(prompt, (chunk: string) => {
      res.write(chunk);
    });

    res.end();
  } catch (error) {
    console.error('Error in explainQuestionController:', error);
    
    if (!res.headersSent) {
      res.status(500).json({ 
        error: 'Internal server error', 
        details: error instanceof Error ? error.message : 'Unknown error' 
      });
    } else {
      res.end();
    }
  }
};
