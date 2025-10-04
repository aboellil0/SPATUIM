import mongoose, { Schema, Document } from 'mongoose';

export interface IMODIS extends Document {
  question: string;
  options: string[];
  correct: string;
  explanation: string;
  createdAt: Date;
  updatedAt: Date;
}

const MODISSchema: Schema = new Schema(
  {
    question: {
      type: String,
      required: true,
    },
    options: {
      type: [String],
      required: true,
    },
    correct: {
      type: String,
      required: true,
    },
    explanation: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true,
    collection: 'MODIS',
  }
);

export default mongoose.model<IMODIS>('MODIS', MODISSchema);
