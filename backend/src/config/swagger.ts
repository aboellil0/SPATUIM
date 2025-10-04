import swaggerJsdoc from 'swagger-jsdoc';
import type { Options } from 'swagger-jsdoc';

const options: Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Terra Chatbot API',
      version: '1.0.0',
      description: 'API documentation for Terra NASA Satellite Chatbot - A specialized assistant that answers questions about NASA\'s Terra Earth Observing Satellite',
      contact: {
        name: 'API Support',
        email: 'support@example.com',
      },
    },
    servers: [
      {
        url: 'http://localhost:3001',
        description: 'Development server',
      },
    ],
    tags: [
      {
        name: 'Message',
        description: 'Terra chatbot messaging endpoints',
      },
      {
        name: 'Health',
        description: 'Server health check endpoints',
      },
    ],
  },
  apis: ['./src/routes/*.ts', './src/server.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
