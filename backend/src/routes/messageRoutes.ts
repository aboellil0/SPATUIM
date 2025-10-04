import { Router } from 'express';
import { messageController, explainQuestionController } from '../controllers/messageController.js';

const router = Router();

/**
 * @swagger
 * /api/message:
 *   post:
 *     summary: Send a message to the Terra chatbot
 *     description: Send a message about NASA's Terra satellite and receive a streaming AI response
 *     tags:
 *       - Message
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - message
 *             properties:
 *               message:
 *                 type: string
 *                 description: Your question or message about Terra satellite
 *                 example: "What is Terra satellite?"
 *     responses:
 *       200:
 *         description: Successful response with AI-generated content
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: "Terra is NASA's flagship Earth Observing System satellite..."
 *       400:
 *         description: Invalid request - message field is required
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   example: "Invalid request"
 *                 details:
 *                   type: string
 *                   example: "Message field is required and must be a string"
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   example: "Internal server error"
 *                 details:
 *                   type: string
 *                   example: "Error details"
 */
router.post('/message', messageController);

/**
 * @swagger
 * /api/explain-question:
 *   post:
 *     summary: Get an explanation for an incorrect quiz answer
 *     description: Send the question details and get an AI explanation of why the user's answer was incorrect and why the correct answer is right
 *     tags:
 *       - Message
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - question
 *               - userAnswer
 *               - correctAnswer
 *             properties:
 *               question:
 *                 type: string
 *                 description: The quiz question text
 *                 example: "What year was Terra satellite launched?"
 *               userAnswer:
 *                 type: string
 *                 description: The answer the user selected
 *                 example: "2001"
 *               correctAnswer:
 *                 type: string
 *                 description: The correct answer to the question
 *                 example: "1999"
 *               options:
 *                 type: array
 *                 description: Optional array of all available answer options
 *                 items:
 *                   type: string
 *                 example: ["1997", "1999", "2001", "2003"]
 *     responses:
 *       200:
 *         description: Successful response with AI-generated explanation
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: "Terra was launched in December 1999, not 2001..."
 *       400:
 *         description: Invalid request - required fields missing
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   example: "Invalid request"
 *                 details:
 *                   type: string
 *                   example: "Question, userAnswer, and correctAnswer fields are required"
 *       500:
 *         description: Internal server error
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   example: "Internal server error"
 *                 details:
 *                   type: string
 *                   example: "Error details"
 */
router.post('/explain-question', explainQuestionController);

export default router;
