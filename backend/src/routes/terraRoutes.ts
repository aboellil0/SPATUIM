import { Router } from 'express';
import {
  getASTERData,
  getCERESData,
  getMODISData,
  getMOPITTData,
  getMISRData,
  getAllTerraData,
  getRandomQuestion
} from '../controllers/terraController.js';

const router = Router();

/**
 * @swagger
 * /api/terra/all:
 *   get:
 *     summary: Get all Terra models data
 *     description: Retrieve all questions from all Terra satellite instruments (ASTER, CERES, MODIS, MOPITT, MISR)
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved all Terra data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *       500:
 *         description: Server error
 */
router.get('/terra/all', getAllTerraData);

/**
 * @swagger
 * /api/terra/aster:
 *   get:
 *     summary: Get all ASTER data
 *     description: Retrieve all questions from the ASTER (Advanced Spaceborne Thermal Emission and Reflection Radiometer) instrument
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved ASTER data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: number
 *                 data:
 *                   type: array
 *       500:
 *         description: Server error
 */
router.get('/terra/aster', getASTERData);

/**
 * @swagger
 * /api/terra/ceres:
 *   get:
 *     summary: Get all CERES data
 *     description: Retrieve all questions from the CERES (Clouds and the Earth's Radiant Energy System) instrument
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved CERES data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: number
 *                 data:
 *                   type: array
 *       500:
 *         description: Server error
 */
router.get('/terra/ceres', getCERESData);

/**
 * @swagger
 * /api/terra/modis:
 *   get:
 *     summary: Get all MODIS data
 *     description: Retrieve all questions from the MODIS (Moderate Resolution Imaging Spectroradiometer) instrument
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved MODIS data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: number
 *                 data:
 *                   type: array
 *       500:
 *         description: Server error
 */
router.get('/terra/modis', getMODISData);

/**
 * @swagger
 * /api/terra/mopitt:
 *   get:
 *     summary: Get all MOPITT data
 *     description: Retrieve all questions from the MOPITT (Measurements of Pollution in the Troposphere) instrument
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved MOPITT data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: number
 *                 data:
 *                   type: array
 *       500:
 *         description: Server error
 */
router.get('/terra/mopitt', getMOPITTData);

/**
 * @swagger
 * /api/terra/misr:
 *   get:
 *     summary: Get all MISR data
 *     description: Retrieve all questions from the MISR (Multi-angle Imaging SpectroRadiometer) instrument
 *     tags:
 *       - Terra
 *     responses:
 *       200:
 *         description: Successfully retrieved MISR data
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 count:
 *                   type: number
 *                 data:
 *                   type: array
 *       500:
 *         description: Server error
 */
router.get('/terra/misr', getMISRData);

/**
 * @swagger
 * /api/terra/random/{model}:
 *   get:
 *     summary: Get a random question from a specific Terra model
 *     description: Retrieve a random question from the specified Terra instrument
 *     tags:
 *       - Terra
 *     parameters:
 *       - in: path
 *         name: model
 *         required: true
 *         schema:
 *           type: string
 *           enum: [ASTER, CERES, MODIS, MOPITT, MISR]
 *         description: The Terra instrument model name
 *     responses:
 *       200:
 *         description: Successfully retrieved random question
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *       400:
 *         description: Invalid model name
 *       404:
 *         description: No data found
 *       500:
 *         description: Server error
 */
router.get('/terra/random/:model', getRandomQuestion);

export default router;
