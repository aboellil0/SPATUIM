import type { Request, Response } from 'express';
import { ASTER, CERES, MODIS, MOPITT, MISR } from '../models/index.js';

// Get all ASTER data
export const getASTERData = async (req: Request, res: Response): Promise<void> => {
  try {
    const data = await ASTER.find();
    res.status(200).json({
      success: true,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Error fetching ASTER data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch ASTER data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get all CERES data
export const getCERESData = async (req: Request, res: Response): Promise<void> => {
  try {
    const data = await CERES.find();
    res.status(200).json({
      success: true,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Error fetching CERES data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch CERES data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get all MODIS data
export const getMODISData = async (req: Request, res: Response): Promise<void> => {
  try {
    const data = await MODIS.find();
    res.status(200).json({
      success: true,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Error fetching MODIS data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch MODIS data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get all MOPITT data
export const getMOPITTData = async (req: Request, res: Response): Promise<void> => {
  try {
    const data = await MOPITT.find();
    res.status(200).json({
      success: true,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Error fetching MOPITT data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch MOPITT data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get all MISR data
export const getMISRData = async (req: Request, res: Response): Promise<void> => {
  try {
    const data = await MISR.find();
    res.status(200).json({
      success: true,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Error fetching MISR data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch MISR data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get all Terra models data
export const getAllTerraData = async (req: Request, res: Response): Promise<void> => {
  try {
    const [aster, ceres, modis, mopitt, misr] = await Promise.all([
      ASTER.find(),
      CERES.find(),
      MODIS.find(),
      MOPITT.find(),
      MISR.find()
    ]);

    res.status(200).json({
      success: true,
      data: {
        ASTER: {
          count: aster.length,
          data: aster
        },
        CERES: {
          count: ceres.length,
          data: ceres
        },
        MODIS: {
          count: modis.length,
          data: modis
        },
        MOPITT: {
          count: mopitt.length,
          data: mopitt
        },
        MISR: {
          count: misr.length,
          data: misr
        }
      }
    });
  } catch (error) {
    console.error('Error fetching all Terra data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch Terra data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

// Get random question from a specific model
export const getRandomQuestion = async (req: Request, res: Response): Promise<void> => {
  try {
    const { model } = req.params;
    
    if (!model) {
      res.status(400).json({
        success: false,
        error: 'Model parameter is required',
        details: 'Please specify a model name in the URL'
      });
      return;
    }
    
    let Model;

    switch (model.toUpperCase()) {
      case 'ASTER':
        Model = ASTER;
        break;
      case 'CERES':
        Model = CERES;
        break;
      case 'MODIS':
        Model = MODIS;
        break;
      case 'MOPITT':
        Model = MOPITT;
        break;
      case 'MISR':
        Model = MISR;
        break;
      default:
        res.status(400).json({
          success: false,
          error: 'Invalid model name',
          details: 'Model must be one of: ASTER, CERES, MODIS, MOPITT, MISR'
        });
        return;
    }

    const count = await Model.countDocuments();
    if (count === 0) {
      res.status(404).json({
        success: false,
        error: 'No data found',
        details: `No questions found in ${model} collection`
      });
      return;
    }

    const random = Math.floor(Math.random() * count);
    const randomQuestion = await Model.findOne().skip(random);

    res.status(200).json({
      success: true,
      data: randomQuestion
    });
  } catch (error) {
    console.error('Error fetching random question:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch random question',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};
