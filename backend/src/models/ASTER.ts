import mongoose, { Schema, Document } from 'mongoose';

export interface IASTER extends Document {
  question: string;
  options: string[];
  correct: string;
  explanation: string;
  createdAt: Date;
  updatedAt: Date;
}

const ASTERSchema: Schema = new Schema(
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
    collection: 'ASTER',
  }
);

export default mongoose.model<IASTER>('ASTER', ASTERSchema);
