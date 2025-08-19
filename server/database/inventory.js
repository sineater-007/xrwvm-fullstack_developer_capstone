'use strict';

const { Schema, model } = require('mongoose');

const CarSchema = new Schema({
  dealer_id: {
    type: Number,
    required: true,
  },
  make: {
    type: String,
    required: true,
    trim: true,
  },
  model: {
    type: String,
    required: true,
    trim: true,
  },
  bodyType: {
    type: String,
    required: true,
    trim: true,
  },
  year: {
    type: Number,
    required: true,
    min: 1886,
    max: new Date().getFullYear(),
  },
  mileage: {
    type: Number,
    required: true,
    min: 0,
  },
});

// Mongoose 会自动把 'Car' → 'cars' 作为集合名
module.exports = model('Car', CarSchema);
