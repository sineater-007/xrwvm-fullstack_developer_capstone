'use strict';

const { Schema, model } = require('mongoose');

const ReviewSchema = new Schema({
  id: {
    type: Number,
    required: true,
    unique: true, // 防止重复 id
  },
  name: {
    type: String,
    required: true,
    trim: true,
  },
  dealership: {
    type: Number,
    required: true,
  },
  review: {
    type: String,
    required: true,
    trim: true,
  },
  purchase: {
    type: Boolean,
    required: true,
  },
  purchase_date: {
    type: Date, // 更合适
    required: true,
  },
  car_make: {
    type: String,
    required: true,
    trim: true,
  },
  car_model: {
    type: String,
    required: true,
    trim: true,
  },
  car_year: {
    type: Number,
    required: true,
    min: 1886, // 世界上第一辆车诞生的年份 😂
  },
});

// Mongoose 会自动用小写复数作为 collection 名：reviews
module.exports = model('Review', ReviewSchema);

