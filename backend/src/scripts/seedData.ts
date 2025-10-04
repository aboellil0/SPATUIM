import mongoose from 'mongoose';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { MODIS, ASTER, CERES, MISR, MOPITT } from '../models/index.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/Terra';

interface QuizQuestion {
  phase: string;
  question: string;
  options: string[];
  correct: string;
  explanation: string;
}

const phaseToModel = {
  'Terra Mission Overview': null, // These go to all collections or we can skip
  'MODIS – Daily Global Imaging': MODIS,
  'ASTER – High-Resolution Imaging': ASTER,
  'CERES – Earth\'s Energy Balance': CERES,
  'MISR – Multi-Angle Observations': MISR,
  'MOPITT – Air Pollution Tracking': MOPITT,
};

async function seedDatabase() {
  try {
    // Connect to MongoDB
    console.log('🔌 Connecting to MongoDB...');
    await mongoose.connect(MONGODB_URI);
    console.log('✅ Connected to MongoDB');

    // Read data.json
    const dataPath = path.join(__dirname, '../../data.json');
    console.log(`📂 Reading data from: ${dataPath}`);
    
    if (!fs.existsSync(dataPath)) {
      console.error('❌ data.json file not found!');
      process.exit(1);
    }

    const rawData = fs.readFileSync(dataPath, 'utf-8');
    const questions: QuizQuestion[] = JSON.parse(rawData);
    console.log(`📊 Found ${questions.length} questions to insert`);

    // Clear existing data
    console.log('🧹 Clearing existing data...');
    await Promise.all([
      MODIS.deleteMany({}),
      ASTER.deleteMany({}),
      CERES.deleteMany({}),
      MISR.deleteMany({}),
      MOPITT.deleteMany({}),
    ]);
    console.log('✅ Existing data cleared');

    // Group questions by phase
    const groupedQuestions: { [key: string]: QuizQuestion[] } = {};
    questions.forEach((q) => {
      if (!groupedQuestions[q.phase]) {
        groupedQuestions[q.phase] = [];
      }
      groupedQuestions[q.phase]!.push(q);
    });

    // Insert questions into appropriate collections
    console.log('📥 Inserting questions into collections...');
    let totalInserted = 0;

    for (const [phase, phaseQuestions] of Object.entries(groupedQuestions)) {
      const model = phaseToModel[phase as keyof typeof phaseToModel];
      
      if (model) {
        const questionsToInsert = phaseQuestions.map(q => ({
          question: q.question,
          options: q.options,
          correct: q.correct,
          explanation: q.explanation,
        }));

        const result = await model.insertMany(questionsToInsert);
        console.log(`  ✅ ${phase}: ${result.length} questions inserted`);
        totalInserted += result.length;
      } else if (phase === 'Terra Mission Overview') {
        // Insert Terra Mission Overview questions into all collections
        const questionsToInsert = phaseQuestions.map(q => ({
          question: q.question,
          options: q.options,
          correct: q.correct,
          explanation: q.explanation,
        }));

        const results = await Promise.all([
          MODIS.insertMany(questionsToInsert),
          ASTER.insertMany(questionsToInsert),
          CERES.insertMany(questionsToInsert),
          MISR.insertMany(questionsToInsert),
          MOPITT.insertMany(questionsToInsert),
        ]);

        const count = results[0].length;
        console.log(`  ✅ ${phase}: ${count} questions inserted into each of 5 collections`);
        totalInserted += count * 5;
      }
    }

    console.log(`\n🎉 Total questions inserted: ${totalInserted}`);

    // Delete data.json file
    console.log('\n🗑️  Deleting data.json file...');
    fs.unlinkSync(dataPath);
    console.log('✅ data.json file deleted successfully');

    // Display final counts
    console.log('\n📊 Final collection counts:');
    const counts = await Promise.all([
      MODIS.countDocuments(),
      ASTER.countDocuments(),
      CERES.countDocuments(),
      MISR.countDocuments(),
      MOPITT.countDocuments(),
    ]);

    console.log(`  • MODIS: ${counts[0]} questions`);
    console.log(`  • ASTER: ${counts[1]} questions`);
    console.log(`  • CERES: ${counts[2]} questions`);
    console.log(`  • MISR: ${counts[3]} questions`);
    console.log(`  • MOPITT: ${counts[4]} questions`);

    console.log('\n✨ Database seeding completed successfully!');

  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  } finally {
    await mongoose.connection.close();
    console.log('🔌 MongoDB connection closed');
    process.exit(0);
  }
}

// Run the seed function
seedDatabase();
